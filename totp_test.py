import pyotp
import base64
import time

def generate_totp_verification():
    print("1. Reading decrypted seed...")
    try:
        with open("decrypted_seed.txt", "r") as f:
            hex_seed = f.read().strip()
    except FileNotFoundError:
        print("ERROR: Run decrypt_test.py first to generate 'decrypted_seed.txt'")
        return

    print(f"   Hex Seed: {hex_seed[:10]}... (hidden)")

    # --- CRITICAL STEP: CONVERSION ---
    # 1. Convert Hex String to Raw Bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # 2. Convert Raw Bytes to Base32 String
    #    (Standard TOTP libraries require Base32)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    print(f"   Base32:   {base32_seed[:10]}... (hidden)")
    # ---------------------------------

    # Create TOTP object
    # Default is SHA-1, 6 digits, 30 seconds - exactly what we need
    totp = pyotp.TOTP(base32_seed)
    
    print("\n2. Generating Codes...")
    print("   Current Time:", time.strftime('%H:%M:%S'))
    print("   Current Code:", totp.now())
    print("   Valid for:    ", totp.interval - (time.time() % totp.interval), "more seconds")

    # Verification Test
    current_code = totp.now()
    is_valid = totp.verify(current_code) 
    print(f"\n   Self-Verification Test: {'PASSED' if is_valid else 'FAILED'}")

if __name__ == "__main__":
    generate_totp_verification()