from fastapi import APIRouter, status, Query, Path, Request, Body, HTTPException, UploadFile, File
from typing import Optional, List, Dict
from pydantic import Field
from uuid import UUID, uuid4
from time import time
from app.models.prediction import Prediction
from app.core.configuration import settings
from app.core.utils import unflatten_spectrogram, load_network
from app.crud.eeg_recordings import retrieve_all_eeg_recordings_data
import csv
import numpy as np


async def get_user_prediction_data(request, eeg_file) -> dict:
  start = time()

  all_eeg_recordings = await retrieve_all_eeg_recordings_data(request)
  no_of_subjects = len(all_eeg_recordings)

  query_file = await eeg_file.read()
  decoded_file = list(map(lambda e: float(e), query_file.decode("utf-8").split(",")))
  query_recording = unflatten_spectrogram(decoded_file)

  datasets = np.zeros((no_of_subjects*6, 2, 36, 54, 1))
  subjects = []
  
  count = 0
  for eeg_recordings in all_eeg_recordings:
    subjects.append(eeg_recordings["user_id"])
    for i in range(6):
      curr_count = count + no_of_subjects*i    
      datasets[curr_count,0,:,:,:] = unflatten_spectrogram(eeg_recordings["eeg_recording_"+str(i+1)])
      datasets[curr_count,1,:,:,:] = query_recording
    count += 1
  
  preds = np.squeeze(request.app.network.predict([datasets[:,0], datasets[:,1]]), axis = -1)
  preds = np.reshape(preds, (6, no_of_subjects))
  
  mean_scores = np.mean(preds, axis=0)
  subject_idx = np.argmin(mean_scores)
  predicted_user_scores = 1.0 - preds[:,subject_idx]

  predicted_user = await request.app.db[settings.user_collection].find_one({
    "user_id": subjects[subject_idx]},
    projection={"_id": False},
  )

  if predicted_user is None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not recognized")

  end = time()

  return {
    "user": predicted_user,
    "user_similarity_scores": predicted_user_scores.tolist(),
    "average_similarity_scores": (1.0 - mean_scores).tolist(),
    "retrieval_time": round(end - start, 4),
    "subject_idx": subject_idx.tolist(),
  }