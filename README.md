# PyArcGIS
Python script for setting up db environment
## Description
This project is to setup environment for ESRI OGC testing.  
It will read input parameters from input text file, and the script will automatically do followings:  
- create two database (common DB & GDB)
- create database connection for DB
- create spatial type for DB
- create enterprise geodatabase for GDB
- create users
## Usage
1. Put all required input parameters in the "input.txt" (default)
2. Run "run.bat" to start - you can modify "run.bat" to set input file path
## Parameters
All parameters are stored in "input.txt" by default, including:  
- db_type  //type of database (ORACLE, POSTGRESQL)  
- ip  //ip address to connect  
- dbname  //database to be connected  
- username  //username  
- password  //password  
- new_dbname  //new database to be created  
- new_gdbname  //new geodatabase to be created  
- sde_filename  //sde file name  
- sde_username  //sde username  
- sde_password  //sde password  
- sde_tbsp  //sde tablespace  
- new_usernames  //new users to be created  
- lib_path  //st_geometry path  
- ecp_path  //enterprise geodatabase authorization file path  
- work_path  //current work path  

__Leave a blank line in the end__
