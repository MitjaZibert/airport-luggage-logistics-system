# ===========================================================================================
# Airport Luggage Logistics System - DB Connection and Util
# ===========================================================================================

# System libraries
import oracledb

import pandas as pd

class DBUtil:

    # Class variables
    db_dns = None
    db_user = None
    db_pass = None

    connection = None
    cursor = None

    # +++++++++++++++++++++++++++
    # Get connection login details
    # +++++++++++++++++++++++++++
    @classmethod
    def define_connection_parameters(cls):
        from read_file import read_file

        # Set Oracle db connector data
        db_config_file = read_file(r'\db_config.ini')
        
        cls.db_dns = db_config_file['Oracle_DB']['dns']
        cls.db_user = db_config_file['Oracle_DB']['user']
        cls.db_pass = db_config_file['Oracle_DB']['pass']
        

    # +++++++++++++++++++++++++++
    # Connect to Oracle DB
    # +++++++++++++++++++++++++++
    @classmethod
    def get_conn(cls):
        
        # Check if db connection parameters are already defined
        if not cls.db_dns:
            cls.define_connection_parameters()

        # Establish the connection
        try:
            cls.connection = oracledb.connect(user=cls.db_user, password=cls.db_pass, dsn=cls.db_dns)
            print("Successfully connected to Oracle Database")
            
            # Create db cursor
            cls.cursor = cls.connection.cursor()
            
        except oracledb.Error as e:
            print("Error while connecting to Oracle Database:", e)


    # +++++++++++++++++++++++++++
    # Close Oracle DB connection
    #++++
    @classmethod
    def close_conn(cls):
        if cls.connection:
            cls.connection.close()
            cls.connection = None
            print("Connection closed.")


    # ===========================================================================================

    # +++++++++++++++++++++++++++
    # DDL commands (CREATE, ALTER, DROP, TRUNCATE)
    #++++

    # Commit db transactions
    @classmethod
    def db_truncate_table(cls, table_name):
        if cls.connection:   
            
            sql = f"TRUNCATE TABLE {table_name}"
            cls.cursor.execute(sql)
            
            print("Truncate completed.")
        else:
            print("Truncate unsuccessful - no connection!")

    # +++++++++++++++++++++++++++
    # DML commands (INSERT, UPDATE, DELETE)
    #++++
    # INSERT db transactions
    @classmethod
    def db_insert(cls, insert_statement, params = None):
        try:
            if params:
                cls.cursor.execute(insert_statement, params)
            else:
                cls.cursor.execute(insert_statement)

        except oracledb.DatabaseError as e:
            print("Error occurred:", e)
        except AttributeError:
            print("Insert unsuccessful - no connection!")


    # INSERT db transactions - from a list (executemany)
    @classmethod
    def db_insert_many(cls, insert_statement, insert_list):
        
        try:
            cls.cursor.executemany(insert_statement, insert_list)

        except oracledb.DatabaseError as e:
            print(insert_statement)
            df = pd.DataFrame(insert_list, columns=['a', 'b', 'c', 'd', 'e'])
            df.to_csv('insert_error.csv', index=False)
            print("Error occurred:", e)
        except AttributeError:
            print("Insert unsuccessful - no connection!")

    # UPDATE db transactions
    @classmethod
    def db_update(cls, update_statement, params = None):
        try: 
            if params:
                cls.cursor.execute(update_statement, params)
            else:
                cls.cursor.execute(update_statement)

        except oracledb.DatabaseError as e:
            print("Error occurred:", e)
        except AttributeError:
            print("Insert unsuccessful - no connection!")


    # +++++++++++++++++++++++++++
    # DQL commands (SELECT)
    #++++
    # QUERY DB
    @classmethod
    def db_query(cls, sql, params = None):
        
        query_result= None
            
        try:
            if params:
                cls.cursor.execute(sql, params)
            else:
                cls.cursor.execute(sql)
            
            query_result = cls.cursor.fetchall()

        except oracledb.DatabaseError as e:
            print("Error occurred:", e)
        except AttributeError:
            print("Insert unsuccessful - no connection!")

        finally:
            return query_result

       

    

    # +++++++++++++++++++++++++++
    # DCL commands (GRANT, REVOKE)
    #++++



    # +++++++++++++++++++++++++++
    # TCL commands (COMMIT, ROLLBACK)
    #++++

    # Commit db transactions
    @classmethod
    def db_commit(cls):
        
        try:
            cls.connection.commit()
            print("Commit completed.")
                  
        except oracledb.DatabaseError as e:
            print("Error occurred:", e)

        except AttributeError:
            print("Insert unsuccessful - no connection!")


    # +++++++++++++++++++++++++++
    # CALL DB PROCEDURES
    #++++
    @classmethod
    def db_procedure_with_return(cls, procedure_name, params_in = None):
        
        # !! 
        # !! BUG - RETURNS: Error occurred: DPY-2010: element 7 is not the same data type as previous elements
        # !! 
        
        try: 
            params = []

            if params_in:
                params.append(params_in)
            
            # Define the OUT parameter as an oracledb variable
            return_value = cls.cursor.var(oracledb.DB_TYPE_VARCHAR, size=5000)  # OUT parameter to capture the return value
            params.append(return_value)
            
            cls.cursor.callproc(procedure_name, params)
            
        except oracledb.DatabaseError as e:
            print("Error occurred:", e)

        except AttributeError:
            print("Insert unsuccessful - no connection!")

        finally:
            return return_value
        
    
    @classmethod
    def db_procedure_no_return(cls, procedure_name, params_in):
        
        try: 
            if params_in:
                cls.cursor.callproc(procedure_name, params_in)
            else:
                cls.cursor.callproc(procedure_name)

        except oracledb.DatabaseError as e:
            print("Error occurred:", e)

        except AttributeError:
            print("Insert unsuccessful - no connection!")
        
    # ===========================================================================================
