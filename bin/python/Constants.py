# import os

class Constants:

    # ODBC Connection
    ENVIORNMENT = 'DEV' # 'DEV' or 'PROD'
    USER_FIRST_NAME = 'HAOYUAN' # Uppercase
    DRIVER = '{ODBC Driver 17 for SQL Server}' # '{ODBC Driver 17 for SQL Server}' '{SQL Server Native Client 11.0}'

    SERVER = '{}-{}'.format(ENVIORNMENT, 'DB')
    DATABASE = '{}_{}'.format(ENVIORNMENT, USER_FIRST_NAME)
        # print(Constants.server, Constants.database)
    
    # EXE paths
    PYTHON_PATH= ''
    WINSCP_PATH= ''

    # Email Notification
    EMAIL_SERVER_IP = '128.171.103.65'
    EMAIL_SERVER_PORT = '25'
    EMAIL_SENDER_ADDR = 'noreply@tasi.org'
    EMAIL_DEV_ADDR = ["vedang@hawaii.edu"]
    EMAIL_CRED_PATH = r'C:\Users\vedang\Vedang\source\repos\TASI_DSSDW\bin\python\email.cred' 
    EMAIL_SECRET_KEY  = r'C:\Users\vedang\Vedang\source\repos\TASI_DSSDW\bin\python\secret.key'

    
    # SFTP
    SFTP_URL= ''
    SSH_KEY_PATH= ''
    SFTP_PRIVATE_KEY_PROD = ''
    SFTP_PRIVATE_KEY_DEV = ''
    

    # Submission Ingest Pipeline
    INGEST_WORKING_DIR= ''
    INGEST_DL_DIR= ''
    INGEST_UL_DIR= ''
    INGEST_UNZIP_RENAME_LOG= ''
    INGEST_META_DRIVER= ''
    INGEST_META_DB= ''
    INGEST_META_TABLE= ''
    INGEST_UPLOAD_LOG= ''
    INGEST_EDI_TYPES = set(("837I", "837P"))
    INGEST_SUPP_TYPES = set(("EOB", "PA", "MA"))


    