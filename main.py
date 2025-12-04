from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import base64
import os
import time
import pyotp
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

app = FastAPI()

# --- CONFIGURATION ---
# In Docker, we map volumes to /data. Locally, we can use a folder named 'data'
DATA_DIR = "/data" if os.path.exists("/data") else "./data"
SEED_FILE = os.path.join(DATA_DIR, "seed.txt")
PRIVATE_KEY_FILE = "student_private.pem"

# Ensure data directory exists locally
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- MODELS ---
class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

# --- HELPER FUNCTIONS ---
def get_decrypted_seed():
    """Reads the decrypted hex seed from storage."""
    if not os.path.exists(SEED_FILE):
        return None
    try:
        with open(SEED_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return None

def get_totp_object(hex_seed: str):
    """Converts hex seed to TOTP object."""
    # Hex -> Bytes -> Base32
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    # Standard: SHA1, 6 digits, 30s interval
    return pyotp.TOTP(base32_seed)

# --- ENDPOINTS ---

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(request: DecryptRequest):
    """
    Accepts base64 encrypted seed, decrypts it, and saves to disk.
    """
    try:
        # 1. Load Private Key
        try:
            with open(PRIVATE_KEY_FILE, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None
                )
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Private key not found on server")

        # 2. Decode Base64 Input
        try:
            encrypted_data = base64.b64decode(request.encrypted_seed)
        except:
            raise HTTPException(status_code=400, detail="Invalid base64 string")

        # 3. Decrypt using RSA-OAEP
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # 4. Save Decrypted Hex Seed Persistence
        decrypted_seed = decrypted_data.decode('utf-8')
        
        # Validate format (must be hex)
        try:
            int(decrypted_seed, 16)
        except ValueError:
             raise HTTPException(status_code=500, detail="Decrypted data is not valid hex")

        with open(SEED_FILE, "w") as f:
            f.write(decrypted_seed)
            
        return {"status": "ok"}

    except Exception as e:
        # Return 500 on decryption failure as per requirements
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

@app.get("/generate-2fa")
def generate_2fa_endpoint():
    """
    Generates current TOTP code based on stored seed.
    """
    hex_seed = get_decrypted_seed()
    if not hex_seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    try:
        totp = get_totp_object(hex_seed)
        code = totp.now()
        
        # Calculate remaining seconds in current 30s window
        valid_for = 30 - int(time.time() % 30)
        
        return {
            "code": code,
            "valid_for": valid_for
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify-2fa")
def verify_2fa_endpoint(request: VerifyRequest):
    """
    Verifies a code with +/- 1 period tolerance.
    """
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")
        
    hex_seed = get_decrypted_seed()
    if not hex_seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        
    try:
        totp = get_totp_object(hex_seed)
        # Verify with valid_window=1 (allows current, previous, and next period)
        is_valid = totp.verify(request.code, valid_window=1)
        
        return {"valid": is_valid}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))