from fastapi import Request
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.cart import cart_item_count


def page_context(request: Request, db: Session, **extra):
    return {
        "request": request,
        "cart_count": cart_item_count(request),
        "current_user": get_current_user(request, db),
        **extra,
    }
