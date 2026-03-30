from fastapi import FastAPI, requests, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

###CC: What Is My IP
app = FastAPI()
apiUrl = "https://fastapi-myproj.rahtiapp.fi/rooms"

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.get("/rooms")
def get_rooms(request: Request):
    response = requests.get(apiUrl)
    data = response.json()

    client_ip = request.client.host
    return {
        "client_ip": client_ip,
        "rooms": data
        }