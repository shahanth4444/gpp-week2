import base64
import subprocess
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# --- CONFIGURATION ---
STUDENT_PRIVATE_KEY = "student_private.pem"
INSTRUCTOR_PUBLIC_KEY = "instructor_public.pem"
REPO_URL = "https://github.com/shahanth4444/gpp-week2" # Verify this is correct

def generate_proof():
    print("Generating Submission Proof...")
    
    # 1. Get the latest Git Commit Hash
    try:
        commit_hash = subprocess.check_output(
            ["git", "log", "-1", "--format=%H"]
        ).decode('utf-8').strip()
    except Exception as e:
        print(f"Error getting git hash: {e}")
        return

    # 2. Load Your Private Key
    try:
        with open(STUDENT_PRIVATE_KEY, "rb") as f:
            student_private = serialization.load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        print(f"Error: Could not find {STUDENT_PRIVATE_KEY}")
        return

    # 3. Load Instructor Public Key
    try:
        with open(INSTRUCTOR_PUBLIC_KEY, "rb") as f:
            instructor_public = serialization.load_pem_public_key(f.read())
    except FileNotFoundError:
        print(f"Error: Could not find {INSTRUCTOR_PUBLIC_KEY}")
        return

    # 4. Sign the Commit Hash (RSA-PSS)
    # CRITICAL: Sign the ASCII bytes of the hash string
    signature = student_private.sign(
        commit_hash.encode('utf-8'), 
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 5. Encrypt the Signature (RSA-OAEP)
    encrypted_signature = instructor_public.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 6. Encode to Base64 (Single Line)
    final_proof = base64.b64encode(encrypted_signature).decode('utf-8').replace('\n', '')

    print("\n" + "="*60)
    print("             FINAL SUBMISSION DATA")
    print("="*60)
    print(f"\n[1] GitHub Repo URL:\n{REPO_URL}")
    print(f"\n[2] Commit Hash:\n{commit_hash}")
    print(f"\n[3] Encrypted Commit Signature (Copy as ONE line):\n{final_proof}")
    print("\n" + "="*60)

if __name__ == "__main__":
    generate_proof()