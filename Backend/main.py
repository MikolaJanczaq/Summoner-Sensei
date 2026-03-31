from fastapi import FastAPI

from listener.client_listener import get_client_data

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Temporary endpoint just for development
@app.get("/client_data")
async def read_client_data():
    return get_client_data()