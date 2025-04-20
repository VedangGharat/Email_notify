import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet as F
from os.path import isfile
import pyodbc
from typing import List, Tuple, Union
from login_info import login_info as c
from builtins import ValueError

def send_mail(
    reciever_id: Union[str, List[str]], subject: str, body: str
) -> str:

    # Load sender's email credentials (username and password)
    sender_email, sender_password = _load_cred()

    # Fetch reciever email addresses based on the given reciever ID(s)
    reciever_email = [
        _get_reciever_email(id)
        for id in (reciever_id if isinstance(reciever_id, list) else [reciever_id])
    ]
    print(reciever_email)


    msg = MIMEMultipart()
    msg["From"] = c.EMAIL_SENDER_ADDR # Sender's address from login_info

    all_recipients = [] # List to store all recipient addresses


    if True:
        msg["Bcc"] = ", ".join(c.EMAIL_SEN_ADDR)
        all_recipients += c.EMAIL_SEN_ADDR

    # Add reciever emails to the "To" field and recipients list
    msg["To"] = ", ".join(reciever_email)
    all_recipients.extend(reciever_email)
    
    # Set the subject and body of the email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attempting to send the email
    try:
        with smtplib.SMTP(c.EMAIL_SERVER_IP, c.EMAIL_SERVER_PORT) as server:
            server.starttls() # Start TLS encryption for secure communication
            server.login(sender_email, sender_password) # Log in with credentials
            text = msg.as_string() # Convert message to string format

            # Send the email to all recipients
            server.sendmail(sender_email, all_recipients, text)
            # print('done')
            return 0
    except Exception as e:
        # Raise an exception if there's an error during the email sending process
        raise Exception(f"Error sending email for reciever ID {reciever_id}: {str(e)}")


def _load_cred() -> Tuple[str, str]:

    # Check if the encryption key file exists 
    if not isfile(c.EMAIL_SECRET_KEY):
        raise Exception(
            'Fernet decryption key is not detected. Please generate the key with "key_generator.py" and store it in this directory.'
        )

    # Load and read the encryption key from file
    key = open(c.EMAIL_SECRET_KEY, "rb").read()

    # Initialize Fernet with the loaded key
    f = F(key)

    # Decrypt and read raw credentials from the encrypted file
    raw_cred = f.decrypt(open(c.EMAIL_CRED_PATH, "rb").read())

    # Decode credentials into a string and split into username and password
    cred = raw_cred.decode("utf-8").split("\n")

    # Ensure that exactly two lines (username and password) are present in the decrypted file
    if len(cred) != 2:
        raise Exception(
            f"Email Credential file: {c.EMAIL_CRED_PATH} is not formatted properly when decoded. Make sure the username and password are on separate lines prior to encryption."
        )
    # print(cred[0], cred[1])
    return cred[0], cred[1]


def _get_reciever_email(reciever_id: str) -> str:

    # Database connection details from Login_info
    try:
        server = c.SERVER_ADDR_SERVER
        database = c.SERVER_ADDR_DB

        # Establish a database connection
        cnxn = pyodbc.connect(
                r"Driver={ODBC Driver 17 for SQL Server};"
                f"Server={server};"
                f"Database={database};"
                "Trusted_Connection=yes;"
            )

        cursor = cnxn.cursor() # Create a cursor object for executing queries

        # Constructing a unique Reciever_ID path (specific to your system)
        GetDirectory = rf"Submitters\{reciever_id}\837"

        # Query to fetch the reciever's email address from the database table/view
        select_statement = # Query needs to be added based database structure
        query = f"{select_statement} = '{GetDirectory}'"

        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            return row.Email_Address
        else:
            raise ValueError(f"No email found for the reciever ID: {id}") # Raise error if no result found

    except pyodbc.Error as e:
        raise ValueError(f"An error occurred while fetching email for reciever ID {reciever_id}: {e}")

    finally:
        cnxn.close() # Ensure database connection is closed in all cases
