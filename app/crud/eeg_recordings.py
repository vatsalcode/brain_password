from fastapi import APIRouter, status, Query, Path, Request, Body, HTTPException, UploadFile, File
from typing import Optional, List, Dict
from pydantic import Field
from pymongo import ReturnDocument
from uuid import UUID, uuid4
from app.models.eeg_recordings import EEGRecordings, EEGRecordingsInDB
from app.core.configuration import settings
from app.core.utils import create_chunks
import csv


async def retrieve_eeg_recordings_data(request: Request, user_id: UUID):
  eeg_recordings = await request.app.db[settings.eeg_recordings_collection].find_one({
    "user_id": user_id},
    projection={"_id": False},
  )

  if eeg_recordings is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EEG Recordings for the user not found")
  return eeg_recordings


async def retrieve_all_eeg_recordings_data(request: Request) -> list:
  all_eeg_recordings = []
  async for eeg_recordings in request.app.db[settings.eeg_recordings_collection].find(projection={"_id": False}):
    all_eeg_recordings.append(eeg_recordings)

  if len(all_eeg_recordings) == 0:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
  return all_eeg_recordings


async def create_eeg_recordings_data(request: Request, user_id: UUID, eeg_files: List[UploadFile]) -> dict:
  if await request.app.db[settings.eeg_recordings_collection].find_one({"user_id": user_id}, projection={"_id": False}):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="EEG Recordings for the user already exist")

  files = [await f.read() for f in eeg_files]
  decoded_files = [list(map(lambda e: float(e), i.decode("utf-8").split(","))) for i in files]
  eeg_recordings = {"eeg_recording_" + str(i): j for i,j in enumerate(decoded_files, start=1)}

  new_eeg_recordings = await request.app.db[settings.eeg_recordings_collection].insert_one({
    **eeg_recordings,
    "user_id": user_id,
  })


async def update_eeg_recordings_data(request: Request, user_id: UUID, eeg: EEGRecordings):
  updated_eeg_recordings = await request.app.db[settings.eeg_recordings_collection].find_one_and_update(
    {"user_id": user_id},
    {"$set": eeg.dict()},
    projection={"_id": False},
    return_document=ReturnDocument.AFTER,
  )

  if updated_eeg_recordings is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EEG Recordings for the user not found")
  return updated_eeg_recordings


async def delete_eeg_recordings_data(request: Request, user_id: UUID):
  deleted_eeg_recordings = await request.app.db[settings.eeg_recordings_collection].find_one_and_delete(
    {"user_id": user_id},
    projection={"_id": False},
  )

  if deleted_eeg_recordings is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EEG Recordings for the user not found")
  return deleted_eeg_recordings