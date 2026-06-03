from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.api.products import router as products_router
from app.api.orders import router as orders_router

app = FastAPI(
    title="Kcell Store",
    description="Online store for Kcell internship",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def home():
    return {
        "message": "Kcell Store API is running"
    }


@app.get("/shop")
def shop(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/orders-page")
def orders_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context={}
    )