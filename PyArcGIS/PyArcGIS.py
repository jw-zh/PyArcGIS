# Name: PyArcGIS
# Description: ..

# Import system modules
import arcpy, os
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Read input from text
def ReadInput(file_address):
    input_file = open(file_address, "r")
    lines = input_file.readlines()
    input = {}
    for item in lines:
        line = str.split(item, '=')
        input[line[0]] = line[1][:-1]
    return input

def SetupEnvironment(ip, work_path, dbname, username, password, new_dbname, new_usernames, sde, db_type, drop_newusers):
    if db_type == "POSTGRES":
        print("PG_SETUP ...")
        PgSetup(ip, work_path, dbname, username, password, new_dbname, new_usernames, sde, db_type, drop_newusers)
    elif db_type == "ORACLE":
        print(db_type)
    elif db_type == "DB2":
        print(db_type)
    else:
        print("Unidentified DB")

def PgSetup(ip, work_path, dbname, username, password, new_dbname, new_usernames, sde, db_type, drop_newusers = "True"):
    # Configuration
    print("You are going to connect to: " + ip)

    # Connect to postgres and create database
    print("Connect to database ...")
    con = connect(dbname = dbname, user = username, host = ip, password = password)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    print("... Connected.")
    cur = con.cursor()
    print("your dbname is: " + new_dbname)
    print("Create database ...")
    
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '" + new_dbname + "';") # Kill all sessions before drop db
    cur.execute('DROP DATABASE IF EXISTS ' + new_dbname + ';')    # Drop db if exists
    cur.execute('CREATE DATABASE ' + new_dbname + " WITH OWNER=postgres ENCODING='UTF-8' CONNECTION LIMIT=-1")
    
    print("... Done.")
    cur.close()
    con.close()

    # Create database connection
    print("your out_name is: " + sde)
    print("Create database connection ...")
    arcpy.CreateDatabaseConnection_management(work_path, sde, "POSTGRESQL", ip, "DATABASE_AUTH", 
                                              username, password, "SAVE_USERNAME", new_dbname)
    for i in range(arcpy.GetMessageCount()):
        arcpy.AddReturnMessage(i)
    arcpy.AddMessage("... Done. \n")

    # Create spatial type
    print("Create spatial type ...")
    ## Check for the newest update
    sde_address = work_path + sde
    dll_address = work_path + "st_geometry.dll"
    arcpy.CreateSpatialType_management(sde_address, "sde", "None", dll_address)
    for i in range(arcpy.GetMessageCount()):
        arcpy.AddReturnMessage(i)
    arcpy.AddMessage("... Done. \n")

    # Create users.
    print("Create users ...")
    for new_user in new_usernames:
        print("Create user : " + new_user)
        arcpy.CreateDatabaseUser_management(sde_address, "DATABASE_USER", new_user, new_user)
        for i in range(arcpy.GetMessageCount()):
            arcpy.AddReturnMessage(i)
        arcpy.AddMessage("... Done. \n")

        # Create schema and grant to user
        # Connect to postgres
        print("Connect to database ...")
        con = connect(dbname = dbname, user = username, host = ip, password = password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("... Connected.")
        cur = con.cursor()
        print("Create schema ...")
        cur.execute("CREATE SCHEMA " + new_user + " AUTHORIZATION " + new_user + " ;")
        cur.execute("GRANT CONNECT ON DATABASE postgres TO " + new_user + " ;")
        print("... Done.")
        cur.close()
        con.close()

    ## Create enterprise geodatabase
    #print("Create enterprise geodatabase ...")
    #ecp_address = work_path + "Server_Ent_Adv.ecp"
    #arcpy.CreateEnterpriseGeodatabase_management("POSTGRESQL", ip, new_gdbname, "DATABASE_AUTH", username, password, "" , "sde", "sde", "", ecp_address)
    #for i in range(arcpy.GetMessageCount()):
    #    arcpy.AddReturnMessage(i)
    #arcpy.AddMessage("... Done. \n")

    # Clean up file
    os.remove(work_path + sde)

    # Drop new users if needed
    if drop_newusers == 'True':
        print("Drop new users ...")
        for new_user in new_usernames:
            print("Drop user : " + new_user)
        
            # Connect to postgres
            print("Connect to new database ...")
            con = connect(dbname = new_dbname, user = username, host = ip, password = password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            print("... Connected.")
            cur = con.cursor()

            print("Drop schema ...")
            cur.execute("DROP SCHEMA IF EXISTS " + new_user + " ;")

            # Connect to postgres
            print("Connect to database ...")
            con = connect(dbname = dbname, user = username, host = ip, password = password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            print("... Connected.")
            cur = con.cursor()

            print("Drop schema ...")
            cur.execute("DROP SCHEMA IF EXISTS " + new_user + " ;")

            print("Revoke ...")
            cur.execute("REVOKE CONNECT ON DATABASE postgres FROM " + new_user + " ;")

            print("Drop user ...")
            cur.execute("DROP USER IF EXISTS " + new_user + " ;")

            print("... Done.")
            cur.close()
            con.close()


# Startup
print("Setup environment ...")

input = ReadInput("input.txt")

# Global variables
db_type = input['db_type']
ip = input['ip']
#work_path = "C:\\Users\\jian9097\\Documents\\ArcGIS\\Projects\\MyProject\\"
work_path = os.getcwd()
work_path = work_path + '\\'
work_path = work_path.replace('\\', '\\\\')
dbname = input['dbname']
username = input['username']
password = input['password']
new_dbname = input['new_dbname']
new_gdbname = input['new_gdbname']
new_usernames = str.split(input['new_usernames'], ',')
sde = input['sde']
drop_newusers = input['drop_newusers']

#SetupEnvironment(ip, work_path, dbname, username, password, new_dbname, new_usernames, sde, db_type, drop_newusers = "True")
SetupEnvironment(ip, work_path, dbname, username, password, new_dbname, new_usernames, sde, db_type, drop_newusers)