from fastapi import APIRouter, status, Query, Path, Request, Body, HTTPException
from typing import Optional, List, Dict
from pydantic import Field
from pymongo import ReturnDocument
from uuid import UUID, uuid4
from app.models.user import User, UserInDB, UserInUpdate
from app.core.configuration import settings


async def retrieve_user_data(request: Request, user_id: UUID) -> dict:
  user = await request.app.db[settings.user_collection].find_one({
    "user_id": user_id},
    projection={"_id": False},
  )

  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return user


async def create_user_data(request: Request, user: User) -> dict:
  if await request.app.db[settings.user_collection].find_one({
    "email": user.email},
    projection={"_id": False},
  ):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")

  new_user_id = uuid4()
  new_user = await request.app.db[settings.user_collection].insert_one({
    **user.dict(),
    "user_id": new_user_id,
  })

  if new_user.inserted_id is None:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not created")
  return new_user_id


async def update_user_data(request: Request, user_id: UUID, user: UserInUpdate):
  updated_user = await request.app.db[settings.user_collection].find_one_and_update(
    {"user_id": user_id},
    {"$set": dict(filter(lambda e: e[1] != None, user.dict().items()))},
    projection={"_id": False},
    return_document=ReturnDocument.AFTER,
  )

  if updated_user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return updated_user


async def delete_user_data(request: Request, user_id: UUID):
  deleted_user = await request.app.db[settings.user_collection].find_one_and_delete(
    {"user_id": user_id},
    projection={"_id": False},
  )

  if deleted_user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  deleted_eeg_recordings = await request.app.db[settings.eeg_recordings_collection].find_one_and_delete(
    {"user_id": user_id},
    projection={"_id": False},
  )
  return deleted_user