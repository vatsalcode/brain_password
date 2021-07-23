from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from uuid import UUID


class EEGRecordings(BaseModel):
  eeg_recording_1: Optional[List[float]] = Field(None)
  eeg_recording_2: Optional[List[float]] = Field(None)
  eeg_recording_3: Optional[List[float]] = Field(None)
  eeg_recording_4: Optional[List[float]] = Field(None)
  eeg_recording_5: Optional[List[float]] = Field(None)
  eeg_recording_6: Optional[List[float]] = Field(None)


class EEGRecordingsInDB(EEGRecordings):
  user_id: UUID = Field(...)
  subject_id: Optional[int] = Field(None)