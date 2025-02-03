import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet as F
from os.path import isfile
import pyodbc
from typing import List, Tuple, Union
from Constants import Constants as c
from builtins import ValueError

def send_mail(
    provider_id: Union[str, List[str]], subject: str, body: str, dev_flag: bool
) -> str:

    """
    Sends an email to one or more providers based on their IDs.

    Args:
        provider_id (Union[str, List[str]]): A single provider ID or a list of provider IDs.
        subject (str): The subject of the email.
        body (str): The body of the email.
        dev_flag (bool): If True, sends a copy of the email to developers for testing.

    Returns:
        str: A success message if the email is sent successfully.

    Raises:
        Exception: If there is an error during the email sending process.
    """
    
    # Load sender's email credentials (username and password)
    sender_email, sender_password = _load_cred()

    # Fetch provider email addresses based on the given provider ID(s)
    provider_email = [
        _get_provider_email(id)
        for id in (provider_id if isinstance(provider_id, list) else [provider_id])
    ]

    # Drafting the email message

    msg = MIMEMultipart()
    msg["From"] = c.EMAIL_SENDER_ADDR # Sender's address from constants

    all_recipients = [] # List to store all recipient addresses

    # If dev_flag is True, add developers' emails to BCC for testing purposes
    if dev_flag:
        msg["Bcc"] = ", ".join(c.EMAIL_DEV_ADDR)
        all_recipients += c.EMAIL_DEV_ADDR

    # Add provider emails to the "To" field and recipients list
    msg["To"] = ", ".join(provider_email)
    all_recipients.extend(provider_email)
    
    # Set the subject and body of the email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attempting to send the email
    try:
        with smtplib.SMTP(c.EMAIL_SERVER_IP, c.EMAIL_SERVER_PORT) as server:
            server.starttls() # Start TLS encryption for secure communication
            server.ehlo() # Identify ourselves to the SMTP server
            server.login(sender_email, sender_password) # Log in with credentials
            text = msg.as_string() # Convert message to string format

            # Send the email to all recipients
            server.sendmail(sender_email, all_recipients, text)
            return 0
    except Exception as e:
        # Raise an exception if there's an error during the email sending process
        raise Exception(f"Error sending email for provider ID {provider_id}: {str(e)}")


def _load_cred() -> Tuple[str, str]:

    """
    Loads and decrypts the email credentials.

    Returns:
        Tuple[str, str]: A tuple containing the sender's email address and password.

    Raises:
        Exception: If the decryption key or credential file is missing or improperly formatted.
    """
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

    return cred[0], cred[1]


def _get_provider_email(provider_id: str) -> str:

    """
    Sends an email to one or more providers based on their IDs.

    Args:
        provider_id (Union[str, List[str]]): A single provider ID or a list of provider IDs.
        subject (str): The subject of the email.
        body (str): The body of the email.
        dev_flag (bool): If True, sends a copy of the email to developers for testing.

    Returns:
        str: A success message if the email is sent successfully.

    Raises:
        Exception: If there is an error during the email sending process.
    """

    # Database connection details from constants
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

        # Constructing a unique Provider_ID path (specific to your system)
        GetDirectory = rf"Submitters\{provider_id}\837"

        # Query to fetch the provider's email address from the database table/view
        select_statement = "SELECT Email_Address from provider_details.dbo.GetDirectory WHERE Provider_ID" # Query needs to be modified based before put into production
        query = f"{select_statement} = '{GetDirectory}'"

        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            return row.Email_Address
        else:
            raise ValueError(f"No email found for the provided ID: {id}") # Raise error if no result found

    except pyodbc.Error as e:
        raise ValueError(f"An error occurred while fetching email for provider ID {provider_id}: {e}")

    finally:
        cnxn.close() # Ensure database connection is closed in all cases
