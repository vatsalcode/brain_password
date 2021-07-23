from pydantic import BaseModel, Field, Json
from typing import Optional, List, Dict, Any


class CustomResponse(BaseModel):
  status_code: int = Field(..., ge=100, le=599)
  message: str = Field(...)


class DataResponse(CustomResponse):
  data: Optional[Any]