import os
from app.db import get_conn
import psycopg
import time
DATABASE_URL = os.getenv("DATABASE_URL")

def create_schema_():
        with get_conn() as conn, conn.cursor() as cur:
              cur.execute("""
                SELECT
                    g.firstname,
                    g.lastname,
                    r.room_number,
                    b.datefrom,
                    b.dateto
                FROM hotel_bookings b
                JOIN hotel_guests g ON b.guest_id = g.id
                        """)