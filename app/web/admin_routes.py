from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.database.db import SessionLocal

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
@router.get("/")
def admin_index(request: Request, db: Session = Depends(get_db)):
    redirect = require_admin(request, db)
    if redirect:
        return redirect

    return RedirectResponse(url="/shop", status_code=303)
