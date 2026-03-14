from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def root():
    return {"message":""}
@app.get("/about")
async def about():
    return{"name": "Мое первое API "}