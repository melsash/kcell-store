from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.cart import (
    add_to_cart,
    build_cart_lines,
    clear_cart,
    decrease_quantity,
    get_cart,
    increase_quantity,
    remove_from_cart,
)
from app.database.db import SessionLocal
from app.models.product import Product
from app.page_context import page_context
from app.services.checkout import create_order_from_cart
from app.templating import templates

router = APIRouter(tags=["Storefront"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cart/add")
def cart_add(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(1),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    add_to_cart(request, product_id, max(quantity, 1))
    return RedirectResponse(url=f"/products/{product_id}", status_code=303)


@router.post("/cart/increase/{product_id}")
def cart_increase(product_id: int, request: Request):
    increase_quantity(request, product_id)
    return RedirectResponse(url="/cart", status_code=303)


@router.post("/cart/decrease/{product_id}")
def cart_decrease(product_id: int, request: Request):
    decrease_quantity(request, product_id)
    return RedirectResponse(url="/cart", status_code=303)


@router.post("/cart/remove/{product_id}")
def cart_remove(product_id: int, request: Request):
    remove_from_cart(request, product_id)
    return RedirectResponse(url="/cart", status_code=303)


@router.get("/cart")
def cart_page(request: Request, db: Session = Depends(get_db)):
    lines, total = build_cart_lines(request, db)
    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context=page_context(
            request,
            db,
            cart_lines=lines,
            total=total,
        ),
    )


@router.post("/checkout")
def checkout(
    request: Request,
    customer_name: str = Form(...),
    phone_number: str = Form(...),
    db: Session = Depends(get_db),
):
    cart = get_cart(request)
    if not cart:
        return RedirectResponse(url="/cart", status_code=303)

    lines, _ = build_cart_lines(request, db)
    if not lines:
        clear_cart(request)
        return RedirectResponse(url="/cart", status_code=303)

    user = get_current_user(request, db)
    order = create_order_from_cart(
        db=db,
        customer_name=customer_name.strip(),
        phone_number=phone_number.strip(),
        cart=cart,
        user_id=user.id if user else None,
    )
    clear_cart(request)
    return RedirectResponse(
        url=f"/order-success?order_id={order.id}",
        status_code=303,
    )


@router.get("/order-success")
def order_success(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context=page_context(request, db, order_id=order_id),
    )
