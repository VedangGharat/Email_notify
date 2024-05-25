# import os

class Constants:

    # ODBC Connection
    environment = 'DEV' # 'DEV' or 'PROD'
    user_first_name = 'HAOYUAN' # Uppercase
    driver = '{ODBC Driver 17 for SQL Server}' # '{ODBC Driver 17 for SQL Server}' '{SQL Server Native Client 11.0}'

    server = '{}-{}'.format(environment, 'DB')
    database = '{}_{}'.format(environment, user_first_name)
        # print(Constants.server, Constants.database)
    
    # Email Notification
    smtp_server = ''
    port = ''
    sender_email = ''
    reciever_email = ''

    # SFTP
    SFTP_PRIVATE_KEY_PROD = ''
    SFTP_PRIVATE_KEY_DEV = ''

    # Pipeline Dependency
        # pass


    