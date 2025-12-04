Based on your request to make the "Implementation Process & Commands" section appear as "normal text" (consistent with the other headings like "Project Overview"), I have adjusted the header level from a large H1 (#) back to a standard H2 (##).

Here is the final, polished README.md file.

Action:

Open README.md.

Delete everything.

Paste the content below.

Commit and push: git add . && git commit -m "Final readme fix" && git push origin main

Markdown

# Secure Containerized Microservice (PKI & TOTP)

This project implements a secure, containerized microservice that demonstrates enterprise-grade security practices. It handles RSA-OAEP decryption of a secure seed, generates Time-based One-Time Passwords (TOTP), and executes automated auditing via cron jobs.

---

## 📋 Project Overview

The system is designed to:
1.  [cite_start]**Decrypt** a secured seed using a committed RSA private key.
2.  [cite_start]**Generate** 2FA codes using the decrypted seed (SHA-1, 30s period)[cite: 28].
3.  [cite_start]**Persist** data across container restarts using Docker volumes[cite: 9].
4.  [cite_start]**Audit** activity by logging codes every minute via a background cron job[cite: 36].

---

## 🛠️ Technology Stack

* [cite_start]**Language:** Python 3.11 (FastAPI) [cite: 10]
* [cite_start]**Containerization:** Docker & Docker Compose 
* [cite_start]**Cryptography:** RSA-4096, OAEP, SHA-256 
* [cite_start]**Scheduling:** Linux Cron [cite: 35]

---

## 📂 Project Structure

```text
.
├── cron/
│   └── 2fa-cron          # Crontab schedule (LF line endings required)
├── data/                 # Docker volume for seed persistence
├── scripts/
│   └── log_2fa_cron.py   # Script executed by cron to log codes
├── Dockerfile            # Multi-stage build config
├── docker-compose.yml    # Service and volume orchestration
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
├── generate_keys.py      # Script to create RSA keypair
├── get_seed.py           # Script to fetch encrypted seed from API
├── generate_proof.py     # Script to sign commit hash for submission
├── student_private.pem   # Identity Key (Committed for evaluation)
├── student_public.pem    # Identity Public Key
└── encrypted_seed.txt    # The secure challenge seed
🚀 Implementation Process & Commands
This section documents the exact steps and commands used to build and verify this service.

Phase 1: Key Generation & Setup
Generated RSA 4096-bit key pair.

Bash

py generate_keys.py
Fetched the Instructor's Public Key for proof encryption.

Pushed public keys to GitHub to register the repository.

Phase 2: Secure Seed Acquisition
Requested the unique encrypted seed from the Instructor API using get_seed.py.

Note: This required strict URL matching and sanitizing Windows line endings.

Bash

py get_seed.py
Output: encrypted_seed.txt

Phase 3: Docker Deployment
Configured Dockerfile with multi-stage build and UTC timezone.

Configured docker-compose.yml with named volumes for /data and /cron.

Build and Run Command:

Bash

docker-compose up --build -d
🧪 API Verification (Testing)
The service exposes three endpoints on port 8080.

1. Decrypt Seed (POST /decrypt-seed)
Decrypts the seed using the private key and saves it to the persistent volume.

PowerShell

$seed = Get-Content encrypted_seed.txt
Invoke-RestMethod -Uri "http://localhost:8080/decrypt-seed" -Method Post -ContentType "application/json" -Body "{`"encrypted_seed`": `"$seed`"}"
2. Generate Code (GET /generate-2fa)
Returns the current valid TOTP code.

PowerShell

Invoke-RestMethod -Uri "http://localhost:8080/generate-2fa"
3. Verify Code (POST /verify-2fa)
Validates a code with ±1 period tolerance.

PowerShell

Invoke-RestMethod -Uri "http://localhost:8080/verify-2fa" -Method Post -ContentType "application/json" -Body "{`"code`": `"123456`"}"
🕒 Cron Job Verification
The internal cron job runs scripts/log_2fa_cron.py every minute.

To verify logs inside the container:

Bash

docker-compose exec app cat /cron/last_code.txt
🔐 Submission Proof Generation
Generates the cryptographically signed proof required for submission.

Signs the current Git Commit Hash with student_private.pem (RSA-PSS).

Encrypts the signature with instructor_public.pem (RSA-OAEP).

Command:

Bash

py generate_proof.py
⚠️ Security Notice
About student_private.pem: This repository contains the private key student_private.pem.


Why: It is required by the assignment instructions so the evaluator can test the decryption logic within the Docker container.

Security Warning: In a real-world production environment, private keys should never be committed to version control. This key is considered compromised and is used only for this academic exercise.

📝 Submission Details
Repository URL: https://github.com/shahanth4444/gpp-week2

Commit Hash: (Generated via generate_proof.py)

Encrypted Signature: (Generated via generate_proof.py).