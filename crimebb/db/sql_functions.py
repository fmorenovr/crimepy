#!/usr/bin/python

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import pandas as pd
from crimebb.utils import verifyDir

def db_connection(config_file, db_name=None, log=False):
  #Define our connection string
  if db_name is not None:
    conn_string = f"host={config_file['host']} user={config_file['username']} password={config_file['password']} dbname={db_name}"
  else:
    conn_string = f"host={config_file['host']} user={config_file['username']} password={config_file['password']}"

  # print the connection string we will use to connect
  if log:
    print ("Connecting to database\n ->%s" % (conn_string))

  # get a connection, if a connect cannot be made an exception will be raised here
  conn = psycopg2.connect(conn_string)
  #conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
  
  # conn.cursor will return a cursor object, you can use this cursor to perform queries
  if log:
    print( "Connected!\n")
  
  return conn
  
def getDBsSize(config_file, list_dbs):
  conn = db_connection(config_file)
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()
  
  db_dict = {"db_name":[], "size": []}

  for db_name in list_dbs:
      query = f"select pg_size_pretty( pg_database_size('{db_name}') );"
      cursor.execute(query)
      row = cursor.fetchone()
      db_dict["db_name"].append(db_name)
      db_dict["size"].append(str(row[0]))
      print("db:", db_name, "size:", str(row[0]))

  cursor.close()
  conn.close()
  
  return db_dict

def getTableSize(config_file, list_dbs):
  for db_name in list_dbs:
    conn = db_connection(config_file, db_name)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    query = """SELECT relname, 
                    num_elements, 
                    pg_size_pretty(size_bytes) AS size_Mb,  
                    size_bytes 
                    FROM ( 
                      SELECT pg_catalog.pg_namespace.nspname AS schema_name, 
                             relname, 
                             pg_relation_size(pg_catalog.pg_class.oid) AS size_bytes, 
                             reltuples::bigint AS num_elements 
                             FROM pg_catalog.pg_class 
                          JOIN pg_catalog.pg_namespace 
                          ON relnamespace = pg_catalog.pg_namespace.oid  
                 ) t  
            WHERE schema_name NOT LIKE 'pg_%' and schema_name='public' 
            ORDER BY size_bytes DESC;"""
    
    cursor.execute(query)
    colnames = [desc[0] for desc in cursor.description]
    query_results = cursor.fetchall()
    df = pd.DataFrame(query_results, columns=colnames)
    print("db:", db_name, "tables:")
    print(df)

    cursor.close()
    conn.close()

def createDBs(config_file, list_dbs, list_current_dbs):
  conn = db_connection(config_file)
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()
  
  for db_name in list_dbs:
    if (db_name,) not in list_current_dbs:
        query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
        cursor.execute(query)

  cursor.close()
  conn.close()
  print("Conn closed", conn.closed)

def deleteDBs(config_file, list_dbs, list_current_dbs):
  conn = db_connection(config_file)
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()
  
  for db_name in list_dbs:
    if (db_name,) in list_current_dbs:
        query = sql.SQL("DROP DATABASE {}").format(sql.Identifier(db_name))
        cursor.execute(query)

  cursor.close()
  conn.close()
  print("Conn closed", conn.closed)

def listDBs(config_file):
  conn = db_connection(config_file)
  cursor = conn.cursor()

  query = "SELECT datname FROM pg_database;"
  cursor.execute(query)

  list_database = cursor.fetchall()
  cursor.close()
  conn.close()
  print("Conn closed", conn.closed)
  return list_database

def listDBtables(config_file, list_dbs):
  
  tables_dict = {}

  for db_name in list_dbs:
      conn = db_connection(config_file, db_name)
      conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
      cursor = conn.cursor()
      query = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
      cursor.execute(query)
      data = cursor.fetchall()
      data_aux = [a[0] for a in data]
      
      tables_dict[db_name] = data_aux
      
      cursor.close()
      conn.close()

  return tables_dict

