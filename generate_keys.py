from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair():
    # Generate private key: 4096 bits, public exponent 65537
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    # Save Private Key to PEM file
    with open("student_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Generate Public Key
    public_key = private_key.public_key()

    # Save Public Key to PEM file
    with open("student_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("Keys generated: student_private.pem and student_public.pem")

if __name__ == "__main__":
    generate_rsa_keypair()