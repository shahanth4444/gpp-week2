import requests
import json
import time

# --- CONFIGURATION ---
STUDENT_ID = "23a91a05g1"

# USE THIS EXACT URL (WITH TRAILING SLASH)
FINAL_REPO_URL = "https://github.com/shahanth4444/gpp-week2/"

# RAW PUBLIC KEY FILE URL
GITHUB_RAW_URL = "https://raw.githubusercontent.com/shahanth4444/gpp-week2/main/student_public.pem"

# ✔ FIXED: CORRECT API URL (zljo — not zijo)
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"


def get_seed_clean():
    print("1. Downloading key from GitHub...")
    try:
        key_resp = requests.get(GITHUB_RAW_URL)
        if key_resp.status_code != 200:
            print("    ERROR: Could not download key from GitHub. Status:", key_resp.status_code)
            return
        
        raw_key = key_resp.text
        print("    Key downloaded.")
        
        # SANITIZE KEY CONTENT
        clean_key = raw_key.replace('\r\n', '\n').strip()
        
        if not clean_key.endswith('\n'):
            clean_key += '\n'
            
        print("    Key sanitized.")
    except Exception as e:
        print(f"    Error during key download: {e}")
        return

    # SEND API REQUEST
    print(f"2. Sending request to API for ID: {STUDENT_ID}...")
    
    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": FINAL_REPO_URL,
        "public_key": clean_key
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if "encrypted_seed" in data:
                with open("encrypted_seed.txt", "w") as f:
                    f.write(data["encrypted_seed"])
                
                print("\nSUCCESS! ===================================")
                print("Encrypted seed saved to 'encrypted_seed.txt'.")
                print("Proceed to Phase 3: Decryption.")
            else:
                print("Response:", data)
        else:
            print(f"\nERROR: API returned status code {response.status_code}")
            print("Response text:", response.text)
            print("\n--- CRITICAL CHECK ---")
            print("If this failed, issue is likely STUDENT ID or REPO URL mismatch.")

    except Exception as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    get_seed_clean()
