
from fastapi.responses import FileResponse
from fastapi import FastAPI
from routers.simple_router import router as simple_router
from routers.item_router import router as item_router
from routers.depends_router import router as depend_router

app = FastAPI(title="Toy API")
app.include_router(simple_router)
app.include_router(item_router)
app.include_router(depend_router)

@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/test")
async def root():
    return {"message": "Hello World!!"}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("/Users/ctw03918/Documents/Jose/Projects/Tech-Journey/learn/learn_api/static/favicon.ico")