import sys
import os
import time
import base64
import pyotp

# Define paths (Docker container paths)
DATA_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def log_2fa():
    # 1. Read the seed
    if not os.path.exists(DATA_FILE):
        print(f"Error: Seed file not found at {DATA_FILE}", file=sys.stderr)
        return

    try:
        with open(DATA_FILE, "r") as f:
            hex_seed = f.read().strip()
    except Exception as e:
        print(f"Error reading seed: {e}", file=sys.stderr)
        return

    # 2. Generate Code
    try:
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        totp = pyotp.TOTP(base32_seed)
        code = totp.now()
        
        # 3. Get UTC Timestamp
        # CRITICAL: Must use UTC as per requirements
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        
        # 4. Write to Log
        log_entry = f"{timestamp} 2FA Code: {code}\n"
        
        # Append to log file
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
            
        print(f"Logged: {log_entry.strip()}")

    except Exception as e:
        print(f"Error generating code: {e}", file=sys.stderr)

if __name__ == "__main__":
    log_2fa()