import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from get_provider_email_data import get_provider_email
from cryptography.fernet import Fernet as F
from os.path import isfile
from Constants import Constants as c

def send_mail(sender_email, sender_password, receiver_email, subject, body):
    """ Data Check """
    # print(receiver_email)
    
    """Drafting email message"""
    msg = MIMEMultipart()
    msg["From"] = c.EMAIL_SENDER_ADDR
    msg["To"] = ", ".join(receiver_email) 
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    """Performing attempt to send"""
    try:
        with smtplib.SMTP(c.EMAIL_SERVER_IP, c.EMAIL_SERVER_PORT) as server:
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error: unable to send email. {e}")


def notifiable_data(provider_id, subject, body, dev_flag):
    """Fetches provider emails and sends the email"""
    provider_email = [get_provider_email(id) for id in provider_id]

    """ Data Check """
    # print(provider_email, subject, body)
    if dev_flag == True:
        _load_cred(c.EMAIL_DEV_ADDR, subject, body)
        _load_cred(provider_email, subject, body)
    else:
        _load_cred(provider_email, subject, body)


def _load_cred(provider_email, subject, body):

    # Check if the secret key file exists
    if not isfile(c.EMAIL_SECRET_KEY):
        raise Exception('Fernet decryption key is not detected. Please generate the key with "key_generator.py" and store it in this directory.')

    # Load the encryption key
    key = open(c.EMAIL_SECRET_KEY, "rb").read()
    f = F(key)
    
    # Read and decrypt the credentials
    raw_cred = f.decrypt(open(c.EMAIL_CRED_PATH, "rb").read())
    
    # Decode the credentials and split into username and password
    cred = raw_cred.decode("utf-8").split('\n')
    
    # Ensure credentials are formatted correctly
    if len(cred) != 2:
        raise Exception(f"Email Credential file: {c.EMAIL_CRED_PATH} is not formatted properly when decoded. Make sure the username and password are on separate lines prior to encryption.")
    
    """credentials check for debugging (username, password)"""
    # print(f"Username: {cred[0]}")
    # print(f"Password: {cred[1]}")
    
    # Return the credentials (username, password)
    send_mail(cred[0], cred[1], provider_email, subject, body)

