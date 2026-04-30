from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

#tillfällig databas
temp_rooms = [
    {room_number: 101, room_type: "single room", price: 100},
    {room_number: 102, room_type: "double room", price: 150},
    {room_number: 103, room_type: "suite", price: 300},
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Booking API!"}

@app.get("/rooms")
def get_rooms():
    return temp_rooms