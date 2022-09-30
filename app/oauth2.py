from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, models, database_config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from schemas import envs


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = envs.secret_key
ALGORITHM = envs.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(envs.access_token_expire_minutes)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get('user_email')

        if not user_email:
            raise credential_exception
        
        token_data = schemas.TokenData(user_email=user_email)
    except JWTError:
        raise credential_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database_config.get_db)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credential', headers={'WWW-Authenticate': 'Brarer'})

    token_data = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.email == token_data.user_email).first()

    return user
