import logging
import os
import time

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.api.products import router as products_router
from app.api.orders import router as orders_router
from app.cart import build_cart_lines
from app.database.init_db import init_db
from app.database.migrate_users import migrate_user_roles
from app.database.seed_admin import seed_admin_if_missing
from app.database.seed_products import seed_products_if_empty
from app.database.db import SessionLocal
from app.models.product import Product
from app.templating import templates
from app.web.admin_routes import router as admin_router
from app.web.auth_routes import router as auth_router
from app.web.routes import router as storefront_router
from app.page_context import page_context

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kcell Store",
    description="Online store for Kcell internship",
    version="1.0.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "kcell-store-dev-secret-change-in-production"),
)

app.include_router(storefront_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.on_event("startup")
def on_startup() -> None:
    for attempt in range(1, 11):
        try:
            init_db()
            migrate_user_roles()
            seed_admin_if_missing()
            seed_products_if_empty()
            return
        except OperationalError:
            if attempt == 10:
                raise
            logger.warning(
                "Database not ready (attempt %d/10); retrying in 2s...",
                attempt,
            )
            time.sleep(2)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Kcell Store API is running"
    }


@app.get("/shop")
def shop(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=page_context(
            request,
            db,
            products=products,
        ),
    )


@app.get("/orders-page")
def orders_page(request: Request, db: Session = Depends(get_db)):
    cart_lines, total = build_cart_lines(request, db)
    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context=page_context(
            request,
            db,
            cart_lines=cart_lines,
            total=total,
        ),
    )
