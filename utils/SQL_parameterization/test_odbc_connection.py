import pyodbc

# User-defined class: Constants.py
from Constants import Constants as C

connection = pyodbc.connect(
    'DRIVER=' + C.driver + 
    ';SERVER=' + C.server + 
    ';DATABASE=' + C.database + 
    ';Trusted_Connection=yes' 
)

# print(    
#     'DIVER=' + C.driver + 
#     ';SERVER=' + C.server + 
#     ';DATABASE=' + C.database + 
#     ';Trusted_Connection=yes' 
#     )

# TODO try

cursor = connection.cursor()

cursor.execute("SELECT TOP(1) * FROM DEV_HAOYUAN.DATA_QUALITY_STG.EE_CLIENT_FEATURE;") # has to be double quotation

rows = cursor.fetchall()
for row in rows:
    print(row)