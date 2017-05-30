### test xml
#import xml.etree.cElementTree as ET

#tree = ET.ElementTree(file = 'test.xml')
#root = tree.getroot()
#print(root[0].tag)
#for child in root:
#    print(child.tag, child.items)

#for elem in tree.iter():
#    print(elem.tag)

class DBTool(Interface):

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    db_type

class PgTool(DBTool):

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    #class members
    db_type
    ip_address
    db_name
    username
    password
    new_db_name
    new_db_tablespace
    new_gdb_name
    new_usernames
    sde_filename
    sde_tablespace

    @classmethod
    def SetupEnvironment():
        pass

    def ReadSettings():
        pass
    def CreateDataBase():
        pass
    def CreateDataBaseConnection():
        pass
    def CreateSpatialType():
        pass
    def CreateEnterpriseGeodatabase():
        pass
    def CreateUsers():
        pass


class OracleTool(DBTool):

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)
    
    @classmethod
    def SetupEnvironment():
        pass

    def ReadSettings():
        pass
    def CreateDataBase():
        pass
    def CreateDataBaseConnection():
        pass
    def CreateSpatialType():
        pass
    def CreateEnterpriseGeodatabase():
        pass
    def CreateUsers():
        pass

class Interface:

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def ReadSettings():
        pass
    def CreateDataBase():
        pass
    def CreateDataBaseConnection():
        pass
    def CreateSpatialType():
        pass
    def CreateEnterpriseGeodatabase():
        pass
    def CreateUsers():
        pass
