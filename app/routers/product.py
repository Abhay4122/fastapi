from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, oauth2
from database_config import engine, get_db


router = APIRouter(prefix='/post', tags=['Posts'])


@router.get('', response_model=List[schemas.ProdcutOut])
async def get_posts(
        db: Session = Depends(get_db),
        get_current_user: str = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ''
    ):
    '''
        Get the list of product with pagination
    '''
    # data = db.query(models.Product).filter(models.Product.name.contains(search)).limit(limit).offset(skip).all()

    data = db.query(models.Product, func.count(models.Vote.user_id).label('votes')).join(
        models.Vote,
        models.Product.id == models.Vote.product_id,
        isouter=True
    ).group_by(models.Product.id).filter(models.Product.name.contains(search)).limit(limit).offset(skip).all()

    return data


@router.get('/{id}', response_model=schemas.ProdcutOut)
async def get_post(id: int, db: Session = Depends(get_db), get_current_user: str = Depends(oauth2.get_current_user)):
    
    product = db.query(models.Product, func.count(models.Vote.user_id).label('votes')).join(
        models.Vote,
        models.Product.id == models.Vote.product_id,
        isouter=True
    ).group_by(models.Product.id).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product with ID: {id} was not found')
    
    return product


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_post(new_post: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(**new_post.dict())
    
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Product)
def update_post(id: int, changable_post: schemas.ProductCreate, db: Session = Depends(get_db), get_current_user: str = Depends(oauth2.get_current_user)):
    modl = models.Product
    product = db.query(modl).filter(modl.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product with ID: {id} was not found')
    
    product.update(changable_post.dict(), synchronize_session=False)
    db.commit()

    return product.first()



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), get_current_user: str = Depends(oauth2.get_current_user)):
    modl = models.Product
    product = db.query(modl).filter(modl.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')
    
    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)