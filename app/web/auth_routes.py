from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user, hash_password, login_user, logout_user, verify_password
from app.database.db import SessionLocal
from app.models.user import User
from app.page_context import page_context
from app.templating import templates

router = APIRouter(tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/register")
def register_page(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse(url="/profile", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=page_context(request, db),
    )


@router.post("/register")
def register_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if get_current_user(request, db):
        return RedirectResponse(url="/profile", status_code=303)

    normalized_email = email.strip().lower()
    if not normalized_email or len(password) < 8:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context=page_context(
                request,
                db,
                error="Please provide a valid email and a password of at least 8 characters.",
            ),
            status_code=400,
        )

    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context=page_context(
                request,
                db,
                error="An account with this email already exists.",
            ),
            status_code=400,
        )

    user = User(
        email=normalized_email,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    login_user(request, user.id)
    return RedirectResponse(url="/profile", status_code=303)


@router.get("/login")
def login_page(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse(url="/profile", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=page_context(request, db),
    )


@router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    normalized_email = email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context=page_context(
                request,
                db,
                error="Invalid email or password.",
            ),
            status_code=400,
        )

    login_user(request, user.id)
    return RedirectResponse(url="/profile", status_code=303)


@router.get("/logout")
def logout(request: Request):
    logout_user(request)
    return RedirectResponse(url="/shop", status_code=303)


@router.get("/profile")
def profile_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context=page_context(request, db, profile_user=user),
    )
