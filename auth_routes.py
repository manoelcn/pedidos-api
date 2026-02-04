from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from main import bcrypt_context
from models import User
from schemas import UserSchema


auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def home():
    return {'message': 'auth'}


@auth_router.post('/users')
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
