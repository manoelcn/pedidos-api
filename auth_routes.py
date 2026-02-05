from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from models import User
from schemas import UserSchema, LoginSchema


auth_router = APIRouter(prefix='/auth', tags=['auth'])


def create_token(user_id: int, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    info_dict = {'sub': str(user_id), 'exp': expiration_date}
    jwt_encoded = jwt.encode(info_dict, SECRET_KEY, ALGORITHM)
    return jwt_encoded

def authenticate_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user

@auth_router.get('/')
async def home():
    return {'message': 'auth'}


@auth_router.post('/create')
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail='user already registered')
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypted_password, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {'message': 'successfully registered user'}


@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail='user not found')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }


@auth_router.post('/login/form')
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail='user not found')
    else:
        access_token = create_token(user.id)
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }


@auth_router.get('/refresh')
async def renew_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }
