from fastapi import APIRouter, status, Query, Path, Request, Response, Body, HTTPException
from typing import Optional, List, Dict
from pydantic import Field
from uuid import UUID, uuid4
from app.models.user import User, UserInDB, UserInUpdate
from app.models.response import CustomResponse, DataResponse
from app.crud.user import (
  retrieve_user_data,
  create_user_data,
  update_user_data,
  delete_user_data,
)


router = APIRouter()


@router.get("/get_user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
):
  try:
    user = await retrieve_user_data(request, user_id)
    return DataResponse(
      status_code=status.HTTP_200_OK,
      message="User retrieved successfully",
      data=user,
    )

  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)


@router.post("/register_user", status_code=status.HTTP_201_CREATED)
async def create_user(
  request: Request,
  response: Response,
  user: User = Body(..., embed=True),
):
  try:
    new_user_id = await create_user_data(request, user)
    return DataResponse(
      status_code=status.HTTP_201_CREATED,
      message="User created successfully",
      data={"user_id": new_user_id},
    )

  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)


@router.put("/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
  user: UserInUpdate = Body(..., embed=True),
):
  try:
    updated_user = await update_user_data(request, user_id, user)
    return DataResponse(
      status_code=status.HTTP_200_OK,
      message="User updated successfully",
      data=updated_user,
    )

  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)


@router.delete("/remove_user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
  request: Request,
  response: Response,
  user_id: UUID = Path(...),
):
  try:
    deleted_user = await delete_user_data(request, user_id)
    return DataResponse(
      status_code=status.HTTP_200_OK,
      message="User deleted successfully",
      data={"user_id": deleted_user["user_id"]},
    )

  except HTTPException as e:
    response.status_code = e.status_code
    return CustomResponse(status_code=e.status_code, message=e.detail)