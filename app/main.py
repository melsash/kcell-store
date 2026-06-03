from fastapi import FastAPI
from app.api.products import router as products_router

app = FastAPI(
    title="Kcell Store",
    description="Online store for Kcell internship",
    version="1.0.0"
)

app.include_router(products_router)

@app.get("/")
def home():
    return {"message": "Kcell Store API is running"}