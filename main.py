# import streamlit as st
# import hashlib
# from cryptography.fernet import Fernet

# # --- Initialize global variables ---
# if 'stored_data' not in st.session_state:
#     st.session_state.stored_data = {}
# if 'failed_attempts' not in st.session_state:
#     st.session_state.failed_attempts = 0
# if 'authorized' not in st.session_state:
#     st.session_state.authorized = False  # Set default to False to ensure security at start
# if 'cipher' not in st.session_state:
#     st.session_state.cipher = Fernet(Fernet.generate_key())  # Generate and store the key once

# cipher = st.session_state.cipher

# # --- Helper functions ---
# def hash_passkey(passkey: str) -> str:
#     """Hashes the passkey using SHA256."""
#     return hashlib.sha256(passkey.encode()).hexdigest()

# def encrypt_data(text: str) -> str:
#     """Encrypts the provided text."""
#     return cipher.encrypt(text.encode()).decode()

# def decrypt_data(encrypted_text: str) -> str:
#     """Decrypts the provided encrypted text."""
#     try:
#         return cipher.decrypt(encrypted_text.encode()).decode()
#     except Exception as e:
#         st.error(f"❌ Decryption failed: {e}")
#         return ""

# def reset_attempts():
#     """Resets failed attempts to zero."""
#     st.session_state.failed_attempts = 0

# # --- Streamlit Pages ---
# st.set_page_config(page_title="Secure Data System", layout="centered")
# # --- Inject Custom CSS for Fanta Buttons ---
# st.markdown("""
#     <style>
#     div.stButton > button {
#         background-color: #FF7F00;
#         color: white;
#         font-weight: bold;
#         border-radius: 8px;
#         margin: 5px 0;
#         width: 100%;
#         transition: background-color 0.3s ease;
#     }
#     div.stButton > button:hover {
#         background-color: #e67300;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.title("🛡️ Secure Data Encryption System")

# # menu = ["Home", "Store Data", "Retrieve Data", "Login"]

# st.sidebar.title("🔒 Secure Data System")
# st.sidebar.image("secure.png")

# menu = ["Home", "Store Data", "Retrieve Data", "Login"]
# choice = st.sidebar.radio("🔗 Navigation", menu)
# # st.sidebar.image("secure.png")

# # --- Home Page ---
# if choice == "Home":
#     st.subheader("🏠 Welcome")
#     st.write("🔐 Use this app to securely **store and retrieve encrypted data** with a unique passkey.")
    
#     st.toast("🔑 Please navigate to the Store Data page to begin.")
    
#     st.area_chart([10, 35, 15, 48, 70], use_container_width=True)

# # --- Store Data Page ---
# elif choice == "Store Data":
#     st.subheader("📂 Store Data Securely")

#     user_data = st.text_area("Enter Data")
#     passkey = st.text_input("Enter Passkey", type="password")

#     if st.button("Encrypt & Save"):
#         if user_data and passkey:
#             hashed_key = hash_passkey(passkey)
#             encrypted_text = encrypt_data(user_data)
#             st.session_state.stored_data[encrypted_text] = {
#                 "encrypted_text": encrypted_text,
#                 "passkey": hashed_key
#             }
#             st.success("✅ Data encrypted and stored successfully!")
#             st.code(encrypted_text, language="text")
#         else:
#             st.error("⚠️ Please enter both data and passkey.")

# # --- Retrieve Data Page ---
# elif choice == "Retrieve Data":
#     if not st.session_state.authorized:
#         st.warning("🔐 Authorization required! Please go to Login Page.")
#         st.stop()

#     st.subheader("🔍 Retrieve Your Data")

#     encrypted_text = st.text_area("Enter Encrypted Data")
#     passkey = st.text_input("Enter Passkey", type="password")

#     if st.button("Decrypt"):
#         if encrypted_text and passkey:
#             hashed_key = hash_passkey(passkey)
#             stored_entry = st.session_state.stored_data.get(encrypted_text)

#             if stored_entry and stored_entry["passkey"] == hashed_key:
#                 decrypted = decrypt_data(encrypted_text)
#                 if decrypted:
#                     st.success("✅ Decryption successful!")
#                     st.code(decrypted, language="text")
#                 reset_attempts()
#             else:
#                 st.session_state.failed_attempts += 1
#                 attempts_left = 3 - st.session_state.failed_attempts
#                 st.error(f"❌ Incorrect credentials. Attempts remaining: {attempts_left}")

#                 if st.session_state.failed_attempts >= 3:
#                     st.warning("🔒 Too many failed attempts. Please reauthorize via Login Page...")
#                     st.session_state.authorized = False
#                     st.experimental_rerun()
#         else:
#             st.error("⚠️ Both fields are required.")

# # --- Login Page ---
# elif choice == "Login":
#     st.subheader("🔑 Reauthorization")
#     st.write("🔒 Please enter the master password to access your data.")
#     st.success("🔑 Password: hg12")

#     login_pass = st.text_input("Enter Master Password", type="password")

#     if st.button("Login"):
#         # Ensure the password is securely verified
#         if login_pass == "hg12":  # Change this in production to a more secure method
#             reset_attempts()
#             st.session_state.authorized = True
#             st.success("✅ Login successful! You can now access your data.")
#         else:
#             st.error("❌ Incorrect master password.")
#             st.session_state.failed_attempts += 1

#             # Provide feedback based on attempts
#             if st.session_state.failed_attempts >= 3:
#                 st.warning("⚠️ Too many failed attempts. Please try again later.")

# # --- Footer ---
# st.markdown("---")
# st.text("🛠️ Developed by Hadiqa Gohar | Secure Data Encryption")


import streamlit as st
import hashlib
import sqlite3
from cryptography.fernet import Fernet

# --- Initialize global variables ---
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'authorized' not in st.session_state:
    st.session_state.authorized = False  # Set default to False to ensure security at start
if 'cipher' not in st.session_state:
    st.session_state.cipher = Fernet(Fernet.generate_key())  # Generate and store the key once

cipher = st.session_state.cipher

# --- Helper functions ---
def hash_passkey(passkey: str) -> str:
    """Hashes the passkey using SHA256."""
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text: str) -> str:
    """Encrypts the provided text."""
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    """Decrypts the provided encrypted text."""
    try:
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        st.error(f"❌ Decryption failed: {e}")
        return ""

def reset_attempts():
    """Resets failed attempts to zero."""
    st.session_state.failed_attempts = 0

# --- Database Functions ---
def init_db():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    conn = sqlite3.connect('secure_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS encrypted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encrypted_text TEXT,
            passkey_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(encrypted_text, passkey_hash):
    """Save encrypted data to the database."""
    conn = sqlite3.connect('secure_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO encrypted_data (encrypted_text, passkey_hash)
        VALUES (?, ?)
    ''', (encrypted_text, passkey_hash))
    conn.commit()
    conn.close()

def retrieve_from_db(encrypted_text):
    """Retrieve encrypted data from the database."""
    conn = sqlite3.connect('secure_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM encrypted_data WHERE encrypted_text = ?
    ''', (encrypted_text,))
    result = c.fetchone()
    conn.close()
    return result

# Initialize the database
init_db()

# --- Streamlit Pages ---
st.set_page_config(page_title="Secure Data System", layout="centered")
# --- Inject Custom CSS for Fanta Buttons ---
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #FF7F00;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        margin: 5px 0;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #e67300;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Secure Data Encryption System")

st.sidebar.title("🔒 Secure Data System")
st.sidebar.image("secure.png")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.radio("🔗 Navigation", menu)

# --- Home Page ---
if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("🔐 Use this app to securely **store and retrieve encrypted data** with a unique passkey.")
    st.toast("🔑 Please navigate to the Store Data page to begin.")
    st.area_chart([10, 35, 15, 48, 70], use_container_width=True)

# --- Store Data Page ---
elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data")
    passkey = st.text_input("Enter Passkey", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_key = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            save_to_db(encrypted_text, hashed_key)
            st.success("✅ Data encrypted and stored successfully!")
            st.code(encrypted_text, language="text")
        else:
            st.error("⚠️ Please enter both data and passkey.")

# --- Retrieve Data Page ---
elif choice == "Retrieve Data":
    if not st.session_state.authorized:
        st.warning("🔐 Authorization required! Please go to Login Page.")
        st.stop()

    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data")
    passkey = st.text_input("Enter Passkey", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            hashed_key = hash_passkey(passkey)
            stored_entry = retrieve_from_db(encrypted_text)

            if stored_entry and stored_entry[2] == hashed_key:
                decrypted = decrypt_data(encrypted_text)
                if decrypted:
                    st.success("✅ Decryption successful!")
                    st.code(decrypted, language="text")
                reset_attempts()
            else:
                st.session_state.failed_attempts += 1
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect credentials. Attempts remaining: {attempts_left}")

                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts. Please reauthorize via Login Page...")
                    st.session_state.authorized = False
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required.")

# --- Login Page ---
elif choice == "Login":
    st.subheader("🔑 Reauthorization")
    st.write("🔒 Please enter the master password to access your data.")
    st.success("🔑 Password: hg12")

    login_pass = st.text_input("Enter Master Password", type="password")

    if st.button("Login"):
        if login_pass == "hg12":  # Change this in production to a more secure method
            reset_attempts()
            st.session_state.authorized = True
            st.success("✅ Login successful! You can now access your data.")
        else:
            st.error("❌ Incorrect master password.")
            st.session_state.failed_attempts += 1

            if st.session_state.failed_attempts >= 3:
                st.warning("⚠️ Too many failed attempts. Please try again later.")

# --- Footer ---
st.markdown("---")
st.text("🛠️ Developed by Hadiqa Gohar | Secure Data Encryption")