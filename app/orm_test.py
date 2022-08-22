from fastapi import FastAPI, Depends, Response, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .database_config import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def root():
    return {'msg': 'Welcome to the fastapi'}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)