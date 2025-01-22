import pyodbc


def get_provider_email(provider_id):
    # print(provider_id)
    try:
        # Establish connection to the SQL Server
        server = 'VEDANG-LAPTOP'  # Server name
        database = 'provider_details'  # Database name
        username = ''  # Leave blank for Windows Authentication
        password = ''  # Leave blank for Windows Authentication (or provide password for SQL Server Authentication)

        # Choose between Windows Authentication or SQL Server Authentication based on the presence of username and password
        if username and password:
            # Using SQL Server Authentication (with username and password)
            cnxn = pyodbc.connect(
                r"Driver={ODBC Driver 17 for SQL Server};"
                f"Server={server};"
                f"Database={database};"
                f"UID={username};"  # User ID for SQL Authentication
                f"PWD={password};"  # Password for SQL Authentication
            )
        else:
            # Using Windows Authentication (no password required)
            cnxn = pyodbc.connect(
                r"Driver={ODBC Driver 17 for SQL Server};"
                f"Server={server};"
                f"Database={database};"
                "Trusted_Connection=yes;"
            )


        cursor = cnxn.cursor()

        PROVIDER_ID = f"Submitters\{provider_id}\837"
        # print(PROVIDER_ID)
        query = f"SELECT Email_Address FROM provider_details.dbo.GetDirectory WHERE Provider_ID = '{PROVIDER_ID}'"
        # print(query)

        # Execute the query with provider_id  as a parameter
        cursor.execute(query)

        # Fetch one result
        row = cursor.fetchone()

        if row:
            # If a result is found, return the email address
            return row.Email_Address
        else:
            # If no result is found, return a message
            return "No email found for the provided ID."

    except pyodbc.Error as e:
        return f"An error occurred: {e}"

    finally:
        # Close the connection
        cnxn.close()

