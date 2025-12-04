import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed_verification():
    print("1. Loading private key...")
    try:
        with open("student_private.pem", "rb") as key_file:
            from cryptography.hazmat.primitives import serialization
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    except FileNotFoundError:
        print("ERROR: 'student_private.pem' not found.")
        return

    print("2. Loading encrypted seed...")
    try:
        with open("encrypted_seed.txt", "r") as seed_file:
            encrypted_b64 = seed_file.read().strip()
            encrypted_data = base64.b64decode(encrypted_b64)
    except FileNotFoundError:
        print("ERROR: 'encrypted_seed.txt' not found.")
        return

    print("3. Decrypting...")
    try:
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # The result should be a UTF-8 string containing the hex seed
        decrypted_seed = decrypted_data.decode('utf-8')
        
        print("\nSUCCESS! ================================")
        print(f"Decrypted Seed: {decrypted_seed}")
        print(f"Length: {len(decrypted_seed)} characters (Should be 64)")
        
        # Verify it is hex
        int(decrypted_seed, 16) 
        print("Validation: Valid Hex String")
        
        # Save it purely for your reference (don't commit this!)
        with open("decrypted_seed.txt", "w") as f:
            f.write(decrypted_seed)
            
    except Exception as e:
        print(f"\nDECRYPTION FAILED: {e}")
        print("Possible causes: Wrong private key, corrupted file, or wrong padding parameters.")

if __name__ == "__main__":
    decrypt_seed_verification()