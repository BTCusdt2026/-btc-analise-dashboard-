from fastapi import FastAPI
from radar import radar_institucional

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Radar Institucional Online"}

@app.get("/radar")
def radar():
    data = radar_institucional()
    return data
