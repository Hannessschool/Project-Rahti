from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.db import get_conn
from app.db import create_schema
from datetime import date
import json
import os

###CC: What Is My IP
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#skapa databas_schema
create_schema()

@app.get("/api/ip")
async def get_ip(request: Request):
    client_ip = request.client.host
    return { "ip": client_ip}


@app.get("/ip", response_class=HTMLResponse)
async def get_ip_html(request: Request):
    client_ip = request.client.host
    return f"<h1> Din publika IP-adress är {client_ip} </h1>"


###CC: CSC Rahti Docker Workflow
@app.get("/hello")
def hello():
    return {"msg": f"Morjens Doris"} 

@app.get("/if/{term}")
def if_test(term: str):
    ret_str = "Default message..."
    if (term == "hello"
        or term == "hi"
        or term == "greetings"):

        ret_str = "Hello to you too!"
    elif (term == "morjens" or term == "hej") and 1 == 0:
        ret_str = "Hej på dig med!"
    else:
        ret_str = f"vad betyder {term}?"
    return {"msg": ret_str}
