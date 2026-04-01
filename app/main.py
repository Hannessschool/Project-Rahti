from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
#import json
#import os


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

###tillfällig databas, lösning för hotellbokning 0.1

temp_rooms = [
    { "room_id": 101, "room_name": "Double room", "price": 100},
    { "room_id": 101, "room_name": "Single room", "price": 70},
    { "room_id": 101, "room_name": "Suite", "price": 150}
    ]



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


###CC: Hotellbokning 0.1
#@app.get("/rooms")
#def get_rooms(request: Request):
    #json_path = os.path.join(os.path.dirname(__file__), "rooms.json")
    
    #with open(json_path, "r", encoding="utf-8") as file:
        #data = json.load(file)

    #return data

@app.get("/")
def read_root():
    return { "msg": "Welcome to the hotell booking API"}

##alternativ lösning
@app.get("/rooms")
def rooms():
    return temp_rooms


@app.post("/bookings")
def create_booking():
    return{"msg: Bokning skapad"}  ##skapa bokningar i databasen
