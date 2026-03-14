from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
async def say(name: str):
    return {"name": f"Привет, {name}",
            "your_name": name,}


@app.get("/user/{user_id}")
async def get_user(user_id : int):
    return {"user_id": user_id,
            "name": f"Пользователь #{user_id}"}

@app.get("/{year}/{month}/{day}")
async def get_user(year : int,month: int,day: int):
    return {"data":f"{year}-{month:02d}-{day:02d}"}

@app.get("/calculate")
async def get_user(num1 : float=10, num2: float=10,operation: str = "+"):
        if operation == "+":
            return{"resylt": num1+num2}
        if operation == "-":
            return{"resylt": num1-num2}
        if operation == "*":
            return{"resylt": num1*num2}
        if operation == ":":
            return{"resylt": num1/num2}

@app.get("/search")
async def get_user(q: str = "",limit: int =10):
    return {"query":q,
            "limit":limit,
            "results":[f"Результат{i+1}" for i in range(limit)]}
