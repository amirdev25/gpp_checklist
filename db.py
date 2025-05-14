# supabase_service.py
from sqlalchemy import insert
from config import SUPABASE_DB_URL
from models.models import users
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


engine = create_engine(SUPABASE_DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def with_session(func):
    async def wrapper(*args, **kwargs):
        session = Session()
        try:
            result = await func(session, *args, **kwargs)
            session.commit()
            return result
        except SQLAlchemyError as e:
            session.rollback()
            print(f"[DB ERROR] {e}")
            return None
        finally:
            session.close()
    return wrapper

@with_session
async def save_user(session, user_id: int, full_name: str, phone: str, job: str):
    stmt = insert(users).values(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        job=job,
        created_at=datetime.now(timezone.utc)
    )
    session.execute(stmt)
    print(f"[DB] User {user_id} added.")
