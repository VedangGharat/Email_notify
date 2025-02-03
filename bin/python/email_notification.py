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

    sender_email, sender_password = _load_cred()
    provider_email = [
        _get_provider_email(id)
        for id in (provider_id if isinstance(provider_id, list) else [provider_id])
    ]

    # Drafting Email
    msg = MIMEMultipart()
    msg["From"] = c.EMAIL_SENDER_ADDR

    all_recipients = []
    if dev_flag:
        msg["Bcc"] = ", ".join(c.EMAIL_DEV_ADDR)
        all_recipients += c.EMAIL_DEV_ADDR

    msg["To"] = ", ".join(provider_email)
    all_recipients.extend(provider_email)

    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attemping To Send
    try:
        with smtplib.SMTP(c.EMAIL_SERVER_IP, c.EMAIL_SERVER_PORT) as server:
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            text = msg.as_string()

            server.sendmail(sender_email, all_recipients, text)
            return "Email sent successfully"
    except Exception as e:
        raise Exception(f"Error sending email for provider ID {provider_id}: {str(e)}")


def _load_cred() -> Tuple[str, str]:

    # Decrypting The Username And Password For Email 
    if not isfile(c.EMAIL_SECRET_KEY):
        raise Exception(
            'Fernet decryption key is not detected. Please generate the key with "key_generator.py" and store it in this directory.'
        )

    key = open(c.EMAIL_SECRET_KEY, "rb").read()
    f = F(key)

    raw_cred = f.decrypt(open(c.EMAIL_CRED_PATH, "rb").read())
    cred = raw_cred.decode("utf-8").split("\n")

    if len(cred) != 2:
        raise Exception(
            f"Email Credential file: {c.EMAIL_CRED_PATH} is not formatted properly when decoded. Make sure the username and password are on separate lines prior to encryption."
        )

    return cred[0], cred[1]


def _get_provider_email(provider_id: str) -> str:

    # Logging Into The Database
    try:
        server = c.SERVER_ADDR_SERVER
        database = c.SERVER_ADDR_DB
        username = c.SERVER_ADDR_USERNAME
        password = c.SERVER_ADDR_PASSWD

        if username and password:
            cnxn = pyodbc.connect(
                r"Driver={ODBC Driver 17 for SQL Server};"
                f"Server={server};"
                f"Database={database};"
                f"UID={username};"
                f"PWD={password};"
            )
        else:
            cnxn = pyodbc.connect(
                r"Driver={ODBC Driver 17 for SQL Server};"
                f"Server={server};"
                f"Database={database};"
                "Trusted_Connection=yes;"
            )

        cursor = cnxn.cursor()

        PROVIDER_ID = rf"Submitters\{provider_id}\837"

        # Queryng Database
        select_statement = "SELECT Email_Address from provider_details.dbo.GetDirectory WHERE Provider_ID"
        query = f"{select_statement} = '{PROVIDER_ID}'"

        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            return row.Email_Address
        else:
            raise ValueError(f"No email found for the provided ID: {id}")

    except pyodbc.Error as e:
        raise ValueError(f"An error occurred while fetching email for provider ID {provider_id}: {e}")

    finally:
        cnxn.close()
