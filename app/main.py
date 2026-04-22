import app
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader  
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from app.db import get_conn
from app.db import create_schema
from datetime import date
from markupsafe import escape

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


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def validate_api_key(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail={"error": "Invalid API Key"})
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM hotel_guests
            WHERE api_key = %s
        """, [api_key])
        guest = cur.fetchone()
        if not guest:
            raise HTTPException(status_code=401, detail={"error": "Invalid API Key"})
        return guest

#datamodell för bokning, kan användas i post request
class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date
    info:str

class BookingUpdate(BaseModel):
    stars: conint(ge=1, le=5) # >= 1-5 <=

#första hälsningstest för att säkerställa att API:t fungerar
with get_conn() as conn, conn.cursor() as cur:
    cur.execute("""
            SELECT 'databasen funkar'
        """)
    print(cur.fetchone())

#första hälsningstest för att säkerställa att API:t fungerar
@app.get("/")
def read_root():
    return { "msg": "Welcome to the hotell booking API"}

#första hälsningstest för att säkerställa att API:t fungerar
@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version() ")
        result = cur.fetchone()
        return {"msg": f"Hotel API!", "db_status": result }


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



#lista alla bokningar
@app.get("/bookings")
def get_bookings(guest: dict = Depends(validate_api_key)):
    print(guest)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 
                r.room_number,
                g.firstname || ' ' || g.lastname AS guest_name,
                (b.dateto - b.datefrom) AS nights,
                r.price as price_per_night,
                CASE 
                    WHEN (b.dateto - b.datefrom) >= 7 THEN 
                        -- 20 percent discount
                        (b.dateto - b.datefrom) * r.price * 0.8
                    ELSE (b.dateto - b.datefrom) * r.price
                END as total_price,
                b.*
            FROM bookings b
            INNER JOIN rooms r
                ON r.id = b.room_id
            INNER JOIN guests g
                ON g.id = b.guest_id
            WHERE b.guest_id = %s
            ORDER BY id
        """, [guest['id']])  ##säkerställ att endast bokningar för den inloggade gästen returneras
    bookings = cur.fetchall()
    return bookings


#Skapa bokningar i databasen, returnera id på den nya bokningen
@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
           INSERT INTO hotel_bookings (
                guest_id, 
                room_id,
                datefrom, 
                dateto
                ) VALUES (
                    %s, 
                    %s, 
                    %s, 
                    %s
                ) RETURNING id
        """, (
            booking.guest_id, 
            booking.room_id,
            booking.datefrom,
            booking.dateto
            ))
        new_booking = cur.fetchone()
    return {"msg": "Booking made", "id": booking.room_id}  ##skapa bokningar i databasen

##
@app.put("/bookings")
def update_booking(id: int, booking: BookingUpdate):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
           UPDATE hotel_bookings SET
                stars = %s, 
           WHERE id = %s
                AND guest_id = %s
            RETURNING *
        """, (
            booking.guest_id, 
            booking.room_id,
            booking.datefrom,
            booking.dateto,
            id
            ))
        updated_booking = cur.fetchone()

    return {"msg": "Booking updated", "id": id}  ##skapa bokningar i databasen

