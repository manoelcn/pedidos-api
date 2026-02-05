from models import db
from sqlalchemy.orm import sessionmaker


async def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
