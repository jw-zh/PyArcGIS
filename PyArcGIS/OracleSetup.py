import arcpy, os, cx_Oracle
# Read input from text
def ReadInput(file_address):
    input_file = open(file_address, "r")
    lines = input_file.readlines()
    input = {}
    for item in lines:
        line = str.split(item, '=')
        input[line[0]] = line[1][:-1]
    return input
# Show returning message
def ShowReturningMessage():
    for i in range(arcpy.GetMessageCount()):
        arcpy.AddReturnMessage(i)
    arcpy.AddMessage("... Done. \n")

### test Oracle
## 0. Read input parameters from file
## 1. Create new DB(JIAN_DB) and GDB(JIAN_GDB)
## 2. Create DB connection
## 3. Create spatial type for JIAN_DB
## 4. Create Enterprise GDB for JIAN_GDB
## 5. Create users (a, b, c)

# Startup
print("Setup environment ...")

input = ReadInput("input_oracle.txt")

# Global variables
db_type = input['db_type']
ip = input['ip']
work_path = os.getcwd()
work_path = work_path + '\\'
#work_path = work_path.replace('\\', '\\\\')
dbname = input['dbname']
username = input['username']
password = input['password']
new_dbname = input['new_dbname']
new_gdbname = input['new_gdbname']
new_usernames = str.split(input['new_usernames'], ',')
sde = input['sde']
new_db_tbsp = input['new_db_tbsp']
sde_tbsp = input['sde_tbsp']
drop_newusers = input['drop_newusers']

# Create new DB and GDB
connection = cx_Oracle.connect('sys/sys@dev000861:1521/cdb', mode = cx_Oracle.SYSDBA)
print(connection.version)
cursor = connection.cursor()
print("ALTER PLUGGABLE DATABASE MASTER OPEN READ WRITE ...")
cursor.execute("ALTER PLUGGABLE DATABASE MASTER OPEN READ WRITE")
print("CLONE FROM MASTER ...")
cursor.callproc('DB_CLONE_PLUGGABLE', ('JW_DB','MASTER'))
cursor.callproc('DB_CLONE_PLUGGABLE', ('JW_GDB','MASTER'))
print("... Done.")
print("ALTER PLUGGABLE DATABASE MASTER CLOSE IMMEDIATE ...")
cursor.execute("ALTER PLUGGABLE DATABASE MASTER CLOSE IMMEDIATE")
cursor.execute("SELECT  NAME, OPEN_MODE FROM    v$pdbs ORDER BY  1")
for result in cursor:
    print(result)
cursor.close()
connection.close()

# Delete existing file
try:
    print("delete file " + work_path + sde + " ...")
    os.remove(work_path + sde)
    print('... Done.')
except OSError:
    pass

# Create database connection
print("your out_name is: " + sde)
print("Create database connection ...")
#arcpy.CreateDatabaseConnection_management(work_path, sde, "ORACLE", "dev000861:1521/" + new_dbname + " as sysdba", "DATABASE_AUTH", "sys", "sys")
arcpy.CreateDatabaseConnection_management(work_path, sde, "ORACLE", "dev000861:1521/" + new_dbname, "DATABASE_AUTH", "sys", "sys")
for i in range(arcpy.GetMessageCount()):
    arcpy.AddReturnMessage(i)
arcpy.AddMessage("... Done. \n")

# Create spatial type
print("Create spatial type ...")
## Check for the newest update
sde_address = work_path + sde
dll_address = "/home/ora12c/Oracle12102/product/12.1.0/dbhome_1/bin/libst_shapelib.so"
arcpy.CreateSpatialType_management(sde_address, "sde", "sde", dll_address)
for i in range(arcpy.GetMessageCount()):
    arcpy.AddReturnMessage(i)
arcpy.AddMessage("... Done. \n")

# Create enterprise geodatabase
print("Create enterprise geodatabase ...")
ecp_address = work_path + "Server_Ent_Adv.ecp"
arcpy.CreateEnterpriseGeodatabase_management("ORACLE", "dev000861:1521/" + new_gdbname, "", "DATABASE_AUTH", "sys", "sys", "" , "sde", "sde", "sde_tablespace", ecp_address)
for i in range(arcpy.GetMessageCount()):
    arcpy.AddReturnMessage(i)
arcpy.AddMessage("... Done. \n")

# Create new users
for new_user in new_usernames:
    print("Create user : " + new_user)
    arcpy.CreateDatabaseUser_management(work_path + sde, "DATABASE_USER", new_user, new_user, "", sde_tbsp)
    for i in range(arcpy.GetMessageCount()):
        arcpy.AddReturnMessage(i)
    arcpy.AddMessage("... Done. \n") 

# Clean up file
os.remove(work_path + sde)