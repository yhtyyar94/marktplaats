from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user_routes

app = FastAPI()
app.include_router(user_routes.router)


@app.get("/")
def index():
    return {"Hello": "World"}


models.Base.metadata.create_all(engine)
