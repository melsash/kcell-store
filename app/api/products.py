from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.product import Product
from app.page_context import page_context
from app.schemas.product import ProductCreate, ProductResponse
from app.templating import templates

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


def _wants_html(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "text/html" in accept and "application/json" not in accept.split(",")[0].strip()


@router.get("/{product_id}")
def get_product(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if _wants_html(request):
        return templates.TemplateResponse(
            request=request,
            name="product.html",
            context=page_context(request, db, product=product),
        )

    return ProductResponse.model_validate(product)


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        image=product.image
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product