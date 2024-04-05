from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"