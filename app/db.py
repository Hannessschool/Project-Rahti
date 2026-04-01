import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)



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
                    room_id SERIAL PRIMARY KEY,
                    room_number INT NOT NULL, 
                    room_name VARCHAR(50),
                    price DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT now()
                );        
                        """)

def create_room_scheme():
     with get_conn() as conn, conn.cursor() as cur:
            # Create the schema
            cur.execute("""
                -- sample parent table
                CREATE TABLE IF NOT EXISTS hotel_rooms (
                    room_id SERIAL PRIMARY KEY, 
                    room_name TEXT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
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