import os
from cryptography.fernet import Fernet
import json
import hashlib
import streamlit as st

# using streamlit session state because on every action the script reruns and variable went 0
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "logged_out" not in st.session_state:
    st.session_state.logged_out = False
# storing file name in the variable
KEY_FILE = "secret key"

# writing a function which will generate the key and store it in the secret key file 
def write_key():
    key = Fernet.generate_key()

    # opening keyfile in wb means write bytes becuase the key is in bytes
    with open(KEY_FILE,'wb') as key_file:

        # now using write function to store the key in the file
        key_file.write(key)
# this function will load the key from the file 
def load_key():
    with open(KEY_FILE,'rb') as key:
        return key.read()
        
# applying if condition for varifying the secret key file does not exist already before creating a new one 
if not os.path.exists(KEY_FILE):
    write_key()        

# storing key in a variable
KEY = load_key()

# to enscrypt and dycrypt the data we have to use Fernet(key) and provide key in the parameters so we will
#  store it in a sngle variable called cipher or anything for ease
cipher = Fernet(KEY)

# storing the name of json file 
DATA_FILE = "data.json"

# creating function to load data from  json file
def load_data():
    if  os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE)>0:
        with open(DATA_FILE,'r') as file:
            return json.load(file)
    return{}

# function to send the data into the json file
def save_data(data):
    with open(DATA_FILE,'w') as file:
        json.dump(data,file,indent=4)   

# function to hash the passkey provided by the user using haslib sha256
def hashed_pass(password):
   return hashlib.sha256(password.encode()).hexdigest()
     
# Making a function to encrypt the data
def encrypt_data(user_data):
    return cipher.encrypt(user_data.encode()).decode()

# Making a function to decrypt the data
def decrypt_data(encrypted_data,passkey):
    hashed_passkey  = hashed_pass(passkey)

    # storing the data into a varible to use it further for decryption
    stored_data = load_data()
    for key,value in stored_data.items():
        if value["encrypted_text"] == encrypted_data and value["passkey"] == hashed_passkey:
            return cipher.decrypt(encrypted_data.encode()).decode()
    st.session_state.failed_attempts += 1
    print(st.session_state.failed_attempts)
    return None

# taking master password
def load_master_pass():
    with open("master_password","r") as master_pass_file:
       master_password = master_pass_file.read()
       return hashed_pass(master_password.strip())
master_password = load_master_pass()
print(master_password)

# UI by streamlit
st.title("🔒 Secure Data Encryption System")

# Side bar
menu = ["Home","Store Data","Retrieve Data","Login"]
if st.session_state.logged_out:
    menu.remove("Home")
    menu.remove("Store Data")
    menu.remove("Retrieve Data")
choice = st.sidebar.selectbox("Navigation",menu)

# Home page
if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")    
    user_data=st.text_area("Enter Data:")
    user_pass = st.text_input("Enter passkey:",type="password")
    save_btn=st.button("Encrypt & Save")
    if save_btn:
        if user_data and user_pass:
            hashed_password = hashed_pass(user_pass)
            encrypted_text = encrypt_data(user_data)
            stored_data = load_data()
            stored_data[encrypted_text]={"encrypted_text":encrypted_text,"passkey":hashed_password}
            save_data(stored_data)
            st.warning(f"Here is your encrypted data: {encrypted_text}")
            st.success("✅ Data stored securely!")
        else:
            st.error("⚠️ Both fields are required!")    
elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")
    if st.button("Decrypt"):
        if encrypted_text and passkey:
            decrypted_data = decrypt_data(encrypted_text,passkey)       
            if decrypted_data:
                st.success(f"✅ Decrypted Data: {decrypted_data}")
            else:
                st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}")
                if st.session_state.failed_attempts >= 3:
                    st.session_state.logged_out = True
                    st.rerun()
        else:
            st.error("⚠️ Both fields are required!")            
elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")
    hashed_login_pass = hashed_pass(login_pass)
    print(hashed_login_pass)

    if st.button("Login"):
        if hashed_login_pass == master_password:  # Hardcoded for demo, replace with proper auth
            st.session_state.failed_attempts = 0
            st.session_state.logged_out = False
            st.rerun()
        else:
            st.error("❌ Incorrect password!")            