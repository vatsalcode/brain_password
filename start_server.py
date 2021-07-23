import uvicorn
from app.main import app
from app.core.configuration import settings


if __name__ == "__main__":
  uvicorn.run(app, host=settings.host, port=settings.port)