"""
Version 04/16/2024
Command Line: python -B ingestWrapper.py -j Parameters.yml -sql TEST.sql
"""

import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# print(sys.path)

import yaml
import re
import argparse
import pyodbc

import logging
logging.basicConfig(level=logging.DEBUG, filename='log.log', filemode='w', format="%(asctime)s - %(levelname)s - %(message)s") # TODO double check file mode 'rewrite'

from Constants import Constants as C

ERROR_CD = 1
SUCCESS_CD = 0

class sqlExec:

    def __init__(self):
        self.connection = None
        self.sql_text = None
        logging.debug("sqlExec instance created, no connection established yet.")

    def sql_connection(self):
        try:
            self.connection = pyodbc.connect(
                'DRIVER=' + C.driver + 
                ';SERVER=' + C.server + 
                ';DATABASE=' + C.database + 
                ';Trusted_Connection=yes' 
            )
            logging.info("Database connection established.")
        
        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")
            exit(ERROR_CD)

        return self.connection

    def variable_substitution(self, job_file_name, is_sql):
        try:
            # Read yaml file
            job_file_path = os.path.join(sys.path[0], job_file_name)
            sql_file_path = os.path.join(sys.path[0], is_sql)

            with open(job_file_path, 'r') as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)

            with open(sql_file_path, 'r') as f:
                self.sql_text = f.read()

            # Match 
            for i in range(0,3):

                for key, value in data['TEST'][i].items(): # TODO how to identify or recognize info from diff levels in a yaml file
                    # Construct the regex pattern for each variable
                    pattern = r"<{}>".format(key)

                    # Replace the variable with its corresponding value
                    self.sql_text = re.sub(pattern, value, self.sql_text)

            logging.info("Variable substitution completed.")\
            
        except Exception as e:
            logging.error(f"Error during variable substitution: {e}")
            raise e
        
        return self.sql_text

    def sql_execution(self):
        try:
            if not self.connection:
                self.sql_connection() # Ensure connection is established

            cursor = self.connection.cursor()
            cursor.execute(self.sql_text) # has to be double quotation

            rows = cursor.fetchall()
            for row in rows:
                print(row)
            
            cursor.close()

            logging.info("SQL execution successful and data fetched.")

        except Exception as e:
            logging.error(f"Error executing SQL: {e}")
            raise e
        
    def sql_log(self):
        pass

# print(sys.path)

if __name__ == '__main__':

#     logger = log.log_init(__name__)
    
    parser = argparse.ArgumentParser()
    # parser.add_argument("-e", "--env", help="Environment dev/prod", type=str, required=True)
    parser.add_argument("-j", "--job", help="path of job yaml file", type=str)
    parser.add_argument("-sql", "--sql file", help="path of the sql file passed from outside", type=str)
    
    args = vars(parser.parse_args())
    # env = args["env"]
    job_file_name = args["job"]
    is_sql = args["sql file"]

    sql_exec = sqlExec()
    sql_exec.variable_substitution(job_file_name, is_sql) 
    sql_exec.sql_execution()
    
# TODO log with diff levels, try, yaml file with more complex structure, command lines dev (checked)