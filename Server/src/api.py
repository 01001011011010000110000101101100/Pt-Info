from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import uvicorn

import threading

from models import Patient, DeletePatient
from database_handler import fetch_patients, insert_patient, alert_patient, delete_data, get_banned

app = FastAPI()

REACTIVE_IPS = set()
BANNED_IPS = get_banned()

def get_reactive_ips():
    return REACTIVE_IPS

def get_banned_ips():
    return BANNED_IPS

def get_client_ip(request: Request) -> str:
    direct_ip = request.client.host if request.client else "Unknown"
    if direct_ip in ("127.0.0.1", "::1"):
        cf_ip = request.headers.get("CF-Connecting-IP")
        if cf_ip:
            return cf_ip.strip()
    return direct_ip


@app.middleware("http")
async def block_banned_ips_middleware(request: Request, call_next):
    client_ip = get_client_ip(request)

    if client_ip in BANNED_IPS:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Your IP has been blocked from accessing this server."},
        )

    REACTIVE_IPS.add(client_ip)
    return await call_next(request)


@app.get("/Patients")
async def get_patients() -> list[list[str]]:
    return await fetch_patients()

@app.post("/Patients", status_code=status.HTTP_201_CREATED)
async def upload_patient(patient: Patient):
    if not await insert_patient(patient):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This bed {patient.Bed_Number} is in use."
        )
    return {
        "details" : "The user has inserted successfully.",
        "bed_id" : patient.Bed_Number
    }

@app.put("/Patients", status_code=status.HTTP_204_NO_CONTENT)
async def edit_patient_data(patient: Patient):
    if not await alert_patient(patient):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The bed number {patient.Bed_Number} does not exist."
        )

    return {}

@app.delete("/Patients", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(bed_number: str):
    await delete_data(bed_number)
    return {}


class ServerManager:
    _config: uvicorn.Config | None = None
    _server: uvicorn.Server | None = None
    _server_thread: threading.Thread | None = None
    def run_server(cls):
        cls._config = uvicorn.Config(app=app, host="127.0.0.1", port=2011, proxy_headers=False)
        cls._server = uvicorn.Server(cls._config)
        cls._server.run()
    
    @classmethod
    def launch_server(cls):
        cls._server_thread = threading.Thread(target=lambda obj = cls: cls.run_server(obj), daemon=True)
        cls._server_thread.start()

    @classmethod
    def close_server(cls):
        cls._server.should_exit = True
        cls._server_thread.join()