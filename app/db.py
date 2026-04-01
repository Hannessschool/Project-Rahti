import os
import psycopg
import time

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    for attempt in range(10):
        try:
            return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)
        except Exception as e:
            print(f"Postgres not ready (attempt {attempt+1}/10): {e}")
            time.sleep(1)
    raise Exception("Could not connect to Postgres after 10 attempts")




def create_schema():
        with get_conn() as conn, conn.cursor() as cur:
            # Create the schema
            cur.execute("""
                -- sample parent table
                CREATE TABLE IF NOT EXISTS foo (
                    id SERIAL PRIMARY KEY, -- primary key
                    created_at TIMESTAMP DEFAULT now()
                );
                
                -- sample child table
                CREATE TABLE IF NOT EXISTS bar (
                    id SERIAL PRIMARY KEY,
                    foo_id INT REFERENCES foo(id), -- foreign key
                    created_at TIMESTAMP DEFAULT now()
                );

                -- adding columns after the fact
                ALTER TABLE foo ADD COLUMN IF NOT EXISTS name VARCHAR;
                ALTER TABLE foo ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT now()""")

            cur.execute("""
                -- sample parent table
                CREATE TABLE IF NOT EXISTS hotel_rooms (
                    id SERIAL PRIMARY KEY,
                    room_number INT NOT NULL, 
                    type VARCHAR(100),
                    price DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT now()
                );
                        
                CREATE TABLE IF NOT EXISTS hotel_guests (
                    id SERIAL PRIMARY KEY,
                    firstname VARCHAR(50),
                    lastname VARCHAR(50),
                    addinfo VARCHAR(200),
                    created_at TIMESTAMP DEFAULT now()
                );

                CREATE TABLE IF NOT EXISTS hotel_bookings (
                    id SERIAL PRIMARY KEY,
                    guest_id INT REFERENCES hotel_guests(id),
                    room_id INT REFERENCES hotel_rooms(id),
                    datefrom DATE NOT NULL,
                    dateto DATE NOT NULL,
                    addinfo VARCHAR(200),
                    created_at TIMESTAMP DEFAULT now()
                );""")

