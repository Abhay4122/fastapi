from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database_config import engine, get_db


router = APIRouter(prefix='/vote', tags=['Votes'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def vote(
        vot: schemas.Vote,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ):
    '''
        Vote the product by the user
    '''

    product_query = db.query(models.Product).filter(
        models.Product.id == vot.product_id
    )

    if not product_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not exist"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.product_id == vot.product_id,
        models.Vote.user_id == current_user.id
    )
    
    if (vot.dir == 1):
        if vote_query.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User {current_user.id} has already voted on Product {vot.product_id}'
            )
        new_vote = models.Vote(product_id = vot.product_id, user_id = current_user.id)

        db.add(new_vote)
        db.commit()

        return {'msg': 'Successfully voted'}
    else:
        if not vote_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'msg': 'Successfully deleted vote'}


    data = db.query(models.Product).filter(models.Product.name.contains(search)).limit(limit).offset(skip).all()

    return data