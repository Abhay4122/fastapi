from fastapi import FastAPI, Depends, Response, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .database_config import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def root():
    return {'msg': 'Welcome to the fastapi'}


@app.get('/post', response_model=List[schemas.Product])
async def get_posts(db: Session = Depends(get_db)):
    data = db.query(models.Product).all()

    return data


@app.get('/post/{id}', response_model=schemas.Product)
async def get_post(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product with ID: {id} was not found')
    
    return product


@app.post('/post', status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_post(new_post: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(**new_post.dict())
    
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@app.put('/post/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Product)
def update_post(id: int, changable_post: schemas.ProductCreate, db: Session = Depends(get_db)):
    modl = models.Product
    product = db.query(modl).filter(modl.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product with ID: {id} was not found')
    
    product.update(changable_post.dict(), synchronize_session=False)
    db.commit()

    return product.first()



@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    modl = models.Product
    product = db.query(modl).filter(modl.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')
    
    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)