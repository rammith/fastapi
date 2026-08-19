from fastapi import FastAPI
from register import router as register_router
from login import router as login_router
from users import router as users_router


app=FastAPI()

app.include_router(register_router)
app.include_router(login_router)
app.include_router(users_router)


@app.get("/")
def home():
    return{"message":"Hello Obito"}

@app.get("/about")
def about():
    return{"message":"About Page"}

