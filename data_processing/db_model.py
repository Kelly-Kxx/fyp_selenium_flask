import sqlite3
from sqlite3 import Error
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()

def create_table(conn, table_name, statement):
    try:
        sql = f""" CREATE TABLE IF NOT EXISTS {table_name} ({statement[:-1]});"""
        #print(sql +"\n")
        c = conn.cursor()
        c.execute(sql)
    
    except Error as e:
        print(e)

def insert_one_row_data(conn,table_name,attr,data):
    try:
        cursor = conn.cursor()
        insert_query = f"""INSERT INTO {table_name} ({attr[:-1]}) VALUES({data})"""
        cursor.execute(insert_query)
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

def get_data(conn,cursor,table_name):
    with conn:
        cursor.execute(f"""SELECT * FROM {table_name}""")
        print(cursor.fetchall())    


def database_model():
    pass
