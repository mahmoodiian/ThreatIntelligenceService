from fastapi import FastAPI

from routers import ip_router, user_auth
from settings.database import Base, engine

app = FastAPI()
app.include_router(ip_router.router, tags=['send-ip'])
app.include_router(user_auth.router, tags=['send-ip'])
# Base.metadata.create_all(bind=engine)
