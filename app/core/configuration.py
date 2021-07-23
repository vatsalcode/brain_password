from pydantic import BaseSettings


class Settings(BaseSettings):
  debug_mode: bool = False
  secret: str
  model_path: str
  db_url: str
  db_name: str
  host: str
  port: int
  user_collection: str = "users"
  eeg_recordings_collection: str = "eeg_recordings"

  nfft: int
  noverlap: int
  fs: int
  cmap: str
  figsize_height: float
  figsize_width: float

  margin: float

  class Config:
    env_file = ".env"


settings = Settings()