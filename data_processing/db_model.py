import sqlite3
from sqlite3 import Error
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from db_requirement import item_requirement
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

def create_table(conn, table_name, attr_list):
    try:
        statement = "Equipment_No text PRIMARY KEY ,"
        for attr in attr_list[1:]:
            statement += f"{attr} text,"
        sql = f""" CREATE TABLE IF NOT EXISTS {table_name} ({statement[:-1]});"""
        #print(sql +"\n")
        c = conn.cursor()
        c.execute(sql)
    
    except Error as e:
        print(e)

def insert_one_row_data(conn,table_name,attr_list,data):
    try:
        
        insert_statement = "Equipment_No ,"
        for attr in attr_list[1:]:
            insert_statement += f"{attr},"
        cursor = conn.cursor()
        insert_query = f"""INSERT INTO {table_name} ({insert_statement[:-1]}) VALUES({data})"""
      
        cursor.execute(insert_query)
        conn.commit()
    except sqlite3.Error as error:
        cursor = conn.cursor()
        equip_no = data.split(',')[0]
        compare_query = f"""SELECT * FROM {table_name} WHERE Equipment_No={equip_no}"""
        cursor.execute(compare_query)
        tmp = '('+ data + ')'
        
        fetched_data = cursor.fetchall()[0]
        fetched_data = item_requirement(fetched_data)
       
        if fetched_data != tmp:
            print(fetched_data)
            print(tmp)
        # print(fetched_data '\n')  
        # print(tmp, '\n') 
        # print("Failed to insert data into sqlite table: ", error)

def get_data(conn,cursor,table_name):
    with conn:
        cursor.execute(f"""SELECT * FROM {table_name}""")
        print(cursor.fetchall())    


