from cryptography.fernet import Fernet
from Constants import Constants as c
import os

def generate_key():
    """
    Generates a key and saves it into a file named 'secret.key'
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the previously generated key from 'secret.key'.
    If the file does not exist, generates a new key and saves it.

    Returns:
        key (bytes): The encryption key.
    """
    if not os.path.exists("secret.key"):
        print("Key file 'secret.key' not found. Generating a new one.")
        generate_key()
    
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def generate_email_cred(username: str, password: str) -> None:
    """
    Encrypts email username and password and stores them in an encrypted format.

    Args:
        username (str): The email username to be encrypted.
        password (str): The email password to be encrypted.

    Returns:
        None: This function does not return a value, but it saves the encrypted
        credentials to a file named "email.cred" in the current directory.
    """
    key = load_key()
    encoded_message = f'{username}\n{password}'.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    with open("email.cred", "wb+") as cred_file:
        cred_file.write(encrypted_message)
    print("Encrypted credentials saved to 'email.cred'.")

if __name__ == "__main__":
    # Only call generate_key() if you need to create a new key.
    # generate_key() # Uncomment this line to generate the key if not already done.
    
    generate_email_cred(username='Username', password='Password')
