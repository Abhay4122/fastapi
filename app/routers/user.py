from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database_config import engine, get_db
from ..utils import hash

router = APIRouter(prefix='/user', tags=['Users'])


# @router.get('/users', response_model=List[schemas.User])
@router.get('/')
async def get_posts(db: Session = Depends(get_db)):
    data = db.query(models.User).all()

    return data


# @router.get('/user/{id}', response_model=schemas.User)
@router.get('/{id}')
async def get_post(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with ID: {id} was not found')
    
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_post(new_post: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hash_pwd = hash(new_post.password)
    new_post.password = hash_pwd

    user = models.User(**new_post.dict())
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, changable_post: schemas.UserCreate, db: Session = Depends(get_db)):
    modl = models.User
    user = db.query(modl).filter(modl.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with ID: {id} was not found')
    
    user.update(changable_post.dict(), synchronize_session=False)
    db.commit()

    return user.first()



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    modl = models.User
    user = db.query(modl).filter(modl.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')
    
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)