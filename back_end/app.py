from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from services.db_lookup import lookup_product_by_hash

app = FastAPI(title="QR Verification API")


# -------------------------
# Enable CORS (for React)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Request Model
# -------------------------
class VerifyRequest(BaseModel):
    hash_key: str


# -------------------------
# Build Database Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERIAL_DB_PATH = os.path.join(BASE_DIR, "database", "serials_hashes.db")
PRODUCT_DB_PATH = os.path.join(BASE_DIR, "database", "info_db", "info.db")


# -------------------------
# Health Check Route
# -------------------------
@app.get("/")
def root():
    return {"message": "QR Verification API is running"}


# -------------------------
# Verify Endpoint
# -------------------------
@app.post("/api/verify")
def verify_qr(request: VerifyRequest):

    hash_key = request.hash_key.strip()

    if not hash_key:
        raise HTTPException(status_code=400, detail="Hash key is required")

    result = lookup_product_by_hash(
        qr_hash=hash_key,
        serial_db_path=SERIAL_DB_PATH,
        product_info_db_path=PRODUCT_DB_PATH,
    )

    if not result:
        return {
            "valid": False,
            "message": "Invalid QR Code"
        }

    return {
        "valid": True,
        "data": result
    }