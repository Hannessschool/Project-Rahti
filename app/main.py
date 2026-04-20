from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
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

api_key_header_name = "X-API-Key"
api_key_header = APIKeyHeader(name=api_key_header_name, auto_error=False)

def validate_api_key(api_key: str):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    with get_conn() as conn, conn.cursor() as cur:
    cur.execute("""
        SELECT * FROM guests where api_key = %s
    """, [api_key])
    guest = cur.fetchone()
    if not guest:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return guest

#datamodell för bokning, kan användas i post request
class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

#testa databasen
@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
    cur.execute("SELECT version()")
    result = cur.fetchone()
return {"msg": f"Hotel API!", "db_status": result }

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


##list all rooms
@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT * 
            FROM hotel_rooms
            ORDER by room_number
        """)
    rooms = cur.fetchall()
    return rooms

##get one room by id
@app.get("/rooms/{room_id}")
def get_room(room_id: int):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT * 
                FROM hotel_rooms
                WHERE id = %s
            """, [room_id])  #list här, tuple används också, skriv inte f-strings för kan manipuleras med några citattecken
            room = cur.fetchone()
        return room



@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version() ")
        result = cur.fetchone()
        return {"msg": f"Hotel API!", "db_status": result }
    
@app.get("/guests")
def get_guests():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT * 
            FROM hotel_guests
            WHERE guest_id = %s
            ORDER BY lastname
        """, [guest["id"]])
    guests = cur.fetchall()
    return guests


##@app.get("/")
##def read_root():
    ##return { "msg": "Welcome to the hotell booking API"}

##alternativ lösning
##@app.get("/rooms")
##def rooms():
    ##return temp_rooms

@app.get("/bookings")
def get_bookings(guest: dict = Depends(validate_api_key)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT * 
            FROM hotel_bookings
        """)
    bookings = cur.fetchall()
    return bookings


@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
           INSERT INTO hotel_bookings (
                guest_id, 
                room_id
                datefrom,
                dateto
                ) VALUES (
                    %s, %s, %s ,%s) RETURNING id
        """, (
            booking.guest_id, 
            booking.room_id,
            booking.datefrom,
            booking.dateto
            ))
            new_booking = cur.fetchone()
        return {"msg": "Booking made", "id": new_booking[0]}  ##skapa bokningar i databasen    ##%s används för att undvika sql injection, list eller tuple används för att skicka in variabler i queryn, inte f-strings!
