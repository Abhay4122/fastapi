from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database_config, schemas, models, utils, oauth2


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database_config.get_db), ):
    modl = models.User

    usr = db.query(modl).filter(modl.email == user.username).first()

    if not usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User email OR password not found')
    
    if not utils.verify(user.password, usr.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Password did not match.')
    
    access_token = oauth2.create_access_token(data={'user_email': usr.email})

    return {'access_token': access_token, 'token_type': 'bearer'}