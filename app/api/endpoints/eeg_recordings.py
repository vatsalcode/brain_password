from fastapi import (
  APIRouter, Request, Response,
  status, Path, Body, HTTPException,
  File, UploadFile,
)
from typing import List
from uuid import UUID

from app.core import messages
from app.crud.eeg_recordings import (
  create_eeg_recordings_data,
  retrieve_eeg_recordings_data,
  update_eeg_recordings_data,
  delete_eeg_recordings_data,
)
from app.models.eeg_recordings import EEGRecordings, EEGRecordingsInDB
from app.models.response import CustomResponse, DataResponse


router = APIRouter()


@router.get("/get_eeg_recordings/{user_id}", status_code=status.HTTP_200_OK)
async def retrieve_eeg_recordings(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
):
  try:
    eeg_recordings = await retrieve_eeg_recordings_data(request, user_id)
    return DataResponse(
      status_code=status.HTTP_200_OK,
      message=messages,
      data=eeg_recordings,
    )
  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)
  except e:
    return CustomResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")


@router.post("/register_eeg_recordings/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_eeg_recordings(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
  eeg_files: List[UploadFile] = File(...),
):
  try:
    new_eeg_recordings = await create_eeg_recordings_data(request, user_id, eeg_files)
    return CustomResponse(
      status_code=status.HTTP_201_CREATED,
      message="EEG Recordings for the user created successfully"
    )
  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)
  except e:
    return CustomResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")


@router.put("/update_eeg_recordings/{user_id}", status_code=status.HTTP_200_OK)
async def update_eeg_recordings(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
  eeg_files: List[UploadFile] = File(...),
):
  try:
    updated_eeg_recordings = await update_eeg_recordings_data(request, user_id, eeg)
    return DataResponse(
      status_code=status.HTTP_200_OK,
      message="EEG Recordings for the user updated successfully",
      data=updated_eeg_recordings,
    )
  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)
  except e:
    return CustomResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")


@router.delete("/remove_eeg_recordings/{user_id}", status_code=status.HTTP_200_OK)
async def delete_eeg_recordings(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
):
  try:
    deleted_eeg_recordings = await delete_eeg_recordings_data(request, user_id)
    return DataResponse(
      status_code=status.HTTP_200_OK,
      message="EEG Recodings for the user deleted successfully",
      data={"user_id": deleted_eeg_recordings["user_id"]},
    )
  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)
  except e:
    return CustomResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")