from fastapi import FastAPI
from config.settings import settings

app = FastAPI(title=settings.app_name)
