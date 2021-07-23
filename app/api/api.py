from fastapi import APIRouter
from app.api.endpoints.user import router as user_router
from app.api.endpoints.eeg_recordings import router as eeg_recordings_router
from app.api.endpoints.prediction import router as predict_router


router = APIRouter()

router.include_router(user_router, tags=["User"], prefix="/user")
router.include_router(eeg_recordings_router, tags=["EEG Recordings"], prefix="/eeg_recordings")
router.include_router(predict_router, tags=["Predict"], prefix="/predict")