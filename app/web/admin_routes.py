from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.database.db import SessionLocal
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.page_context import page_context
from app.services.admin_orders import build_order_rows
from app.templating import templates

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
@router.get("/")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    denied = require_admin(request, db)
    if denied:
        return denied

    product_count = db.query(Product).count()
    order_count = db.query(Order).count()
    user_count = db.query(User).count()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context=page_context(
            request,
            db,
            product_count=product_count,
            order_count=order_count,
            user_count=user_count,
        ),
    )


@router.get("/products")
def admin_products_list(request: Request, db: Session = Depends(get_db)):
    denied = require_admin(request, db)
    if denied:
        return denied

    products = db.query(Product).order_by(Product.id).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/products_list.html",
        context=page_context(request, db, products=products),
    )


@router.get("/products/create")
def admin_product_create_form(request: Request, db: Session = Depends(get_db)):
    denied = require_admin(request, db)
    if denied:
        return denied

    return templates.TemplateResponse(
        request=request,
        name="admin/product_form.html",
        context=page_context(
            request,
            db,
            product=None,
            form_title="Create product",
            form_action="/admin/products/create",
        ),
    )


@router.post("/products/create")
def admin_product_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: str = Form(""),
    db: Session = Depends(get_db),
):
    denied = require_admin(request, db)
    if denied:
        return denied

    product = Product(
        name=name.strip(),
        description=description.strip(),
        price=price,
        image=image.strip(),
    )
    db.add(product)
    db.commit()

    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/products/edit/{product_id}")
def admin_product_edit_form(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    denied = require_admin(request, db)
    if denied:
        return denied

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        request=request,
        name="admin/product_form.html",
        context=page_context(
            request,
            db,
            product=product,
            form_title="Edit product",
            form_action=f"/admin/products/edit/{product_id}",
        ),
    )


@router.post("/products/edit/{product_id}")
def admin_product_edit(
    product_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: str = Form(""),
    db: Session = Depends(get_db),
):
    denied = require_admin(request, db)
    if denied:
        return denied

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = name.strip()
    product.description = description.strip()
    product.price = price
    product.image = image.strip()
    db.commit()

    return RedirectResponse(url="/admin/products", status_code=303)


@router.post("/products/delete/{product_id}")
def admin_product_delete(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    denied = require_admin(request, db)
    if denied:
        return denied

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/orders")
def admin_orders_list(request: Request, db: Session = Depends(get_db)):
    denied = require_admin(request, db)
    if denied:
        return denied

    order_rows = build_order_rows(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/orders_list.html",
        context=page_context(request, db, order_rows=order_rows),
    )
