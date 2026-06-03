from fastapi import FastAPI

app = FastAPI(
    title="Kcell Store",
    description="Online store for Kcell internship",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Kcell Store API is running"}