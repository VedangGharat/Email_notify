# version 04/10/2024 Haoyuan Zhang

# TODO How to use command lines to execute SQL scripts on SQL Server
# cd C:\Users\haoyuan.zhang\source\repos\SQL_TEST\SQL_TEST\Parameterization
# sqlcmd -s CMALAN\haoyuan.zhang\DEV-DB -i TEST.sql -o scriptfile.log -E

import yaml
import re

# Read yaml file
with open(r'C:\Users\haoyuan.zhang\source\repos\SQL_TEST\SQL_TEST\Parameterization\Parameters.yml', 'r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
     
# Print the values as a dictionary
# print(data)

# Read sql file
with open(r'C:\Users\haoyuan.zhang\source\repos\SQL_TEST\SQL_TEST\Parameterization\TEST.sql', 'r') as f:
    sql_text = f.read()

# Print the sql file as a text file
# print(sql_text)

# Match 
for i in range(0,3):

    for key, value in data['TEST'][i].items():
        # Construct the regex pattern for each variable
        pattern = r"<{}>".format(key)
        # print(pattern)
        # Replace the variable with its corresponding value
        sql_text = re.sub(pattern, value, sql_text)

print(sql_text)

# Write the modified SQL text to a new file or print it
# with open("output.sql", 'w') as output_file:
#     output_file.write(sql_text)

#print(data['TEST'][1].items())


# variableval = "<VAR_TGT_DB>.<VAR_TGT_SCHEMA>.<VAR_TGT_TBL>"

# tmp = re.match("(.*?)<VAR_(.*?)>", variableval)
# if tmp:
#     for i in re.findall("(.*?)<VAR_(.*?)>", variableval):
#         try:
#             variableval = re.sub("<VAR_"+i+">")

# <VAR_TGT_DB>.<VAR_TGT_SCHEMA>.<VAR_TGT_TBL>

# c:/Users/haoyuan.zhang/source/repos/SQL_TEST/SQL_TEST/.venv/Scripts/python.exe c:/Users/haoyuan.zhang/source/repos/SQL_TEST/SQL_TEST/Parameterization/ingestWrapper.py
# sqlcmd -s CMALAN\haoyuan.zhang\DEV-DB -i output.sql -o scriptfile.log -E