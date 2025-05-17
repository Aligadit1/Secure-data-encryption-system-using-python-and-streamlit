# 🔐 Secure Data Encryption System

A Streamlit-based app to securely **encrypt, store, and retrieve data** using user-defined passkeys. It uses **Fernet encryption**, **SHA-256 hashing**, and **JSON-based storage**.

## 🚀 Features

- Encrypt and save sensitive data locally
- Decrypt data using the correct passkey
- Secure passkey hashing (SHA-256)
- Master password protection
- Tracks failed attempts and locks after 3 failures
- Clean and user-friendly Streamlit UI

## 🛠 Technologies Used

- Python
- Streamlit
- cryptography (Fernet)
- hashlib
- JSON
- os module

## 📁 Files

- `secret key` — stores the generated Fernet key
- `data.json` — encrypted data + hashed passkeys
- `master_password` — stores master password (read and hashed at runtime)

## ▶️ How to Run

1. Clone this repo
2. Install dependencies:
   ```bash
   pip install streamlit cryptography
Create a master_password file with your password.

Run the app:

bash
Copy
Edit
streamlit run your_script.py
✅ Usage
Store Data: Enter your data + a passkey → data gets encrypted and saved.

Retrieve Data: Provide encrypted text + correct passkey → view decrypted data.

After 3 wrong attempts, login with the master password to continue.

⚠️ Note
This is a local demo app. Do not use it for real-world sensitive data
