from fastapi import FastAPI
from backend.app.routes.upload import router as upload_router
from backend.app.routes.analyze import router as analyze_router 

app = FastAPI(title="MyBand API", version="0.1.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "myband-api"}

app.include_router(upload_router, prefix='/api')
app.include_router(analyze_router, prefix="/api")