import cx_Oracle, json
from .Genmst_Appl import Genmst_Appl
from .Genmst import Genmst
from .Obj_Actions import Obj_Actions
from .Obj_Forms import Obj_Forms
from .Obj_Itemchange import Obj_Itemchange
from .Obj_Links import Obj_Links
from .Pophelp import Pophelp
from .Transetup import Transetup
from .Sd_Trans_Design import Sd_Trans_Design
from .GenerateEditMetadataXML import GenerateEditMetadataXML
from .GenerateBrowMetadataXML import GenerateBrowMetadataXML
from .Dynamic_Table_Creation import Dynamic_Table_Creation
import loggerutility as logger
from flask import request
import traceback
import commonutility as common
from DatabaseConnectionUtility import Oracle 
from DatabaseConnectionUtility import Dremio
from DatabaseConnectionUtility import InMemory 
from DatabaseConnectionUtility import Oracle
from DatabaseConnectionUtility import MySql
from DatabaseConnectionUtility import MSSQLServer 
from DatabaseConnectionUtility import SAPHANA
from DatabaseConnectionUtility import Postgress
from DatabaseConnectionUtility import SnowFlake

class Generate_Transcation:

    connection           = None
    schema_name          = ''
    object_name          = ''
    dbDetails            = ''
    transaction_model    = ''
    user_info            = ''

    def get_database_connection(self, dbDetails):        
        if dbDetails != None:
            klass = globals()[dbDetails['DB_VENDORE']]
            dbObject = klass()
            connection_obj = dbObject.getConnection(dbDetails)
                
        return connection_obj

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
                logger.log(f"Transaction committed successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during commit: {error}")
        else:
            logger.log(f"No active connection to commit.")

    def rollback(self):
        if self.connection:
            try:
                self.connection.rollback()
                logger.log(f"Transaction rolled back successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during rollback: {error}")
        else:
            logger.log(f"No active connection to rollback.")

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                logger.log(f"Transaction close successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during close: {error}")
        else:
            logger.log(f"No active connection to close.")

    def genearate_transaction_with_schema(self):

        jsondata =  request.get_data('jsonData', None)
        logger.log(f"\nJsondata inside Generate_Transcation class:::\t{jsondata} \t{type(jsondata)}","0")
        jsondata =  json.loads(jsondata[9:])
        logger.log(f"\nJsondata inside Generate_Transcation class:::\t{jsondata} \t{type(jsondata)}","0")

        if "dbDetails" in jsondata and jsondata["dbDetails"] != None:
            self.dbDetails = jsondata["dbDetails"]
            logger.log(f"\nInside dbDetails value:::\t{self.dbDetails} \t{type(self.dbDetails)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing dbDetails value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)

        if "schema_name" in jsondata and jsondata["schema_name"] != None:
            self.schema_name = jsondata["schema_name"]
            logger.log(f"\nInside schema_name value:::\t{self.schema_name} \t{type(self.schema_name)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing schema_name value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)
        
        if "object_name" in jsondata and jsondata["object_name"] != None:
            self.object_name = jsondata["object_name"]
            logger.log(f"\nInside object_name value:::\t{self.object_name} \t{type(self.object_name)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing object_name value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)

        self.connection = self.get_database_connection(self.dbDetails)
        if self.connection:
            logger.log(f"Inside connection")
            sql = f"SELECT SCHEMA_MODEL FROM sd_trans_design WHERE schema_name='{self.schema_name}'"
            logger.log(f"SQL Query::  {sql}")
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result_lst = cursor.fetchall()
            logger.log(f"result_lst :::::249 {result_lst} {type(result_lst)}")

            if result_lst:
                clob_data = result_lst[0][0]  
                if clob_data is not None:
                    self.transaction_model = json.loads(clob_data.read())
                    logger.log(f"Schema Model Data:\n{self.transaction_model}")
                else:
                    return f"No CLOB data found for the given schema_name."
            else:
                return f"No results returned from the query."
            
            try:
                sql_models = self.transaction_model["transaction"]["sql_models"]

                dynamic_table_creation = Dynamic_Table_Creation()
                dynamic_table_creation.create_alter_table(self.transaction_model, self.connection)

                generatebrowmetadataXML = GenerateBrowMetadataXML()
                generatebrowmetadataXML.jsonData = self.transaction_model
                result = generatebrowmetadataXML.build_xml_str()
                logger.log(f"{result}")

                generateeditmetadataXML = GenerateEditMetadataXML()
                generateeditmetadataXML.jsonData = self.transaction_model
                result = generateeditmetadataXML.build_xml_str()
                logger.log(f"{result}")

                genmst = Genmst()
                genmst.process_data(self.connection, sql_models)

                obj_actions = Obj_Actions()
                obj_actions.process_data(self.connection, sql_models)

                obj_forms = Obj_Forms()
                obj_forms.process_data(self.connection, sql_models, self.object_name)

                obj_links = Obj_Links()
                obj_links.process_data(self.connection, sql_models)

                pophelp = Pophelp()
                pophelp.process_data(self.connection, sql_models)

                transetup = Transetup()
                transetup.process_data(self.connection, sql_models, self.object_name)

                obj_itemchange = Obj_Itemchange()
                obj_itemchange.process_data(self.connection, sql_models)

                self.commit()
                trace = traceback.format_exc()
                descr = str("Transaction successfully created.")
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)
            
            except Exception as e:
                logger.log(f"Rollback successfully.")
                self.rollback()
                
                logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)
            finally:
                logger.log('Closed connection successfully')
                self.close_connection()
        else:
            trace = traceback.format_exc()
            descr = str("Connection fail")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)

    def genearate_transaction_with_model(self):
        # transaction_model,dbDetails,object_name

        jsondata =  request.get_data('jsonData', None)
        jsondata =  json.loads(jsondata[9:])
        logger.log(f"\nJsondata inside Generate_Transcation class:::\t{jsondata} \t{type(jsondata)}","0")

        if "transaction_model" in jsondata and jsondata["transaction_model"] != None:
            self.transaction_model = jsondata["transaction_model"]
            logger.log(f"\nInside transaction_model value:::\t{self.transaction_model} \t{type(self.transaction_model)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing dbDetails value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)
        
        if "dbDetails" in jsondata and jsondata["dbDetails"] != None:
            self.dbDetails = jsondata["dbDetails"]
            logger.log(f"\nInside dbDetails value:::\t{self.dbDetails} \t{type(self.dbDetails)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing schema_name value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)
        
        if "object_name" in jsondata and jsondata["object_name"] != None:
            self.object_name = jsondata["object_name"]
            logger.log(f"\nInside object_name value:::\t{self.object_name} \t{type(self.object_name)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing object_name value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)

        if "schema_name" in jsondata and jsondata["schema_name"] != None:
            self.schema_name = jsondata["schema_name"]
            logger.log(f"\nInside schema_name value:::\t{self.schema_name} \t{type(self.schema_name)}","0")
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Missing schema_name value")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)

        if "user_info" in jsondata and jsondata["user_info"] != None:
            self.user_info = jsondata["user_info"]
            logger.log(f"\nInside user_info value:::\t{self.user_info} \t{type(self.user_info)}","0")
        
        self.connection = self.get_database_connection(self.dbDetails)

        if self.connection:
            try:
                sql_models = self.transaction_model["transaction"]["sql_models"]

                dynamic_table_creation = Dynamic_Table_Creation()
                dynamic_table_creation.create_alter_table(self.transaction_model, self.connection)

                generatebrowmetadataXML = GenerateBrowMetadataXML()
                generatebrowmetadataXML.jsonData = self.transaction_model
                result = generatebrowmetadataXML.build_xml_str()
                logger.log(f"{result}")

                generateeditmetadataXML = GenerateEditMetadataXML()
                generateeditmetadataXML.jsonData = self.transaction_model
                result = generateeditmetadataXML.build_xml_str()
                logger.log(f"{result}")

                genmst = Genmst()
                genmst.process_data(self.connection, sql_models)

                obj_actions = Obj_Actions()
                obj_actions.process_data(self.connection, sql_models)

                obj_forms = Obj_Forms()
                obj_forms.process_data(self.connection, sql_models, self.object_name)

                obj_links = Obj_Links()
                obj_links.process_data(self.connection, sql_models)

                pophelp = Pophelp()
                pophelp.process_data(self.connection, sql_models)

                transetup = Transetup()
                transetup.process_data(self.connection, sql_models, self.object_name)

                obj_itemchange = Obj_Itemchange()
                obj_itemchange.process_data(self.connection, sql_models)

                sd_trans_design = Sd_Trans_Design()
                sd_trans_design.process_data(self.connection, self.user_info, {'schema_name': self.schema_name,'schema_model': json.dumps(self.transaction_model)})

                self.commit()
                trace = traceback.format_exc()
                descr = str("Transaction successfully created.")
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)
            
            except Exception as e:
                logger.log(f"Rollback successfully.")
                self.rollback()
                logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)
            finally:
                logger.log('Closed connection successfully')
                self.close_connection()
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Connection fail")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)

    
