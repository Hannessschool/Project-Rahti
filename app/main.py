<<<<<<< HEAD
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/api/ip")
async def get_ip(request: Request):
    client_ip = request.client.host
    return { "ip": client_ip}


@app.get("/ip", response_class=HTMLResponse)
async def get_ip_html(request: Request):
    client_ip = request.client.host
    return f"<h1> Din publika IP-adress är {client_ip} </h1>"
=======
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Morjens Doris!", "v": "0.1" }


@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}
>>>>>>> 94798ea0c2e975d558923a8ffe9d21d57581802a
