from fastapi import FastAPI

app = FastAPI()


@app.get("/info")
async def root():
    return {"name": "Кирилл",
            "age": "14",
            "favorit_subject":"алгебра"

            }


@app.get("/hobby")
async def about():
    return {"hobby": "прорамитрование"}