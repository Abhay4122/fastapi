from fastapi import FastAPI, Depends, Response, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import models, schemas
from database_config import engine, get_db
from routers import product, user, auth, vote


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def root():
    return {'msg': 'Welcome to the fastapi'}


app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)