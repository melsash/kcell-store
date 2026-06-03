from passlib.context import CryptContext
from fastapi import Request
from sqlalchemy.orm import Session

from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SESSION_USER_ID_KEY = "user_id"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def login_user(request: Request, user_id: int) -> None:
    request.session[SESSION_USER_ID_KEY] = user_id


def logout_user(request: Request) -> None:
    request.session.pop(SESSION_USER_ID_KEY, None)


def get_session_user_id(request: Request) -> int | None:
    user_id = request.session.get(SESSION_USER_ID_KEY)
    if user_id is None:
        return None
    try:
        return int(user_id)
    except (TypeError, ValueError):
        return None


def get_current_user(request: Request, db: Session) -> User | None:
    user_id = get_session_user_id(request)
    if user_id is None:
        return None
    return db.query(User).filter(User.id == user_id).first()
