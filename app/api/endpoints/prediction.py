from fastapi import APIRouter, status, Query, Path, Request, Body, File, UploadFile, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Dict
from pydantic import Field
from app.models.prediction import Prediction
from app.models.response import CustomResponse, DataResponse
from app.core.configuration import settings
from app.crud.prediction import get_user_prediction_data
import numpy as np


router = APIRouter()

  
@router.post("/", status_code=status.HTTP_200_OK)
async def get_user_prediction(
  request: Request,
  response: Response,
  eeg_file: UploadFile = File(...),
):
  try:
    prediction = await get_user_prediction_data(request, eeg_file)

    return DataResponse(
      status_code=status.HTTP_200_OK,
      message="User recognized successfully",
      data=prediction,
    )

  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)