import requests
import time

BASE_URL = "http://localhost:8080"

def test_container():
    print("--- [1] Decrypting Seed ---")
    try:
        # Read the encrypted seed file
        with open("encrypted_seed.txt", "r") as f:
            seed_content = f.read().strip()
            
        # Send to API
        response = requests.post(
            f"{BASE_URL}/decrypt-seed",
            json={"encrypted_seed": seed_content}
        )
        print(f"Status: {response.status_code}")
        print(f"Result: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n--- [2] Generating 2FA Code ---")
    try:
        response = requests.get(f"{BASE_URL}/generate-2fa")
        print(f"Status: {response.status_code}")
        print(f"Result: {response.json()}")
        
        # Save code for verification
        code = response.json().get("code")
    except Exception as e:
        print(f"Error: {e}")
        return

    if code:
        print(f"\n--- [3] Verifying Code {code} ---")
        try:
            response = requests.post(
                f"{BASE_URL}/verify-2fa",
                json={"code": code}
            )
            print(f"Status: {response.status_code}")
            print(f"Result: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

    print("\n--- [4] Checking Cron Job (Wait 70s first!) ---")
    print("Run this command in terminal manually to check cron logs:")
    print("docker-compose exec app cat /cron/last_code.txt")

if __name__ == "__main__":
    test_container()