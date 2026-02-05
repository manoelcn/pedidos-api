from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db, User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker, Session


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        info_dict = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(info_dict.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail='access denied')
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail='access denied')
    return user
