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

def insert_one_row_data(conn,table_name,attr_list,str_data,ori_data):
    try:
        
        insert_statement = "Equipment_No ,"
        for attr in attr_list[1:]:
            insert_statement += f"{attr},"
        cursor = conn.cursor()
        insert_query = f"""INSERT INTO {table_name} ({insert_statement[:-1]}) VALUES({str_data})"""
        cursor.execute(insert_query)
        conn.commit()
        # result = get_one_row_data(cursor, table_name, ori_data[0])
        # print("inserted data", result)
    except sqlite3.Error as error:
        cursor = conn.cursor()
        [same_ID_bool,data_tuple,fetched_data_tuple] = compare_equipID(conn,cursor,table_name,attr_list,ori_data)
        # print("same_ID", same_ID_bool, type(data_tuple[0]), type(fetched_data_tuple[0]))        
        if same_ID_bool: 
            # if(data_tuple != fetched_data_tuple):
                update_data(conn,cursor,data_tuple,attr_list,table_name)
        else:
            t = (str(data_tuple[0]),)
            cursor.execute(f"""SELECT * FROM {table_name} WHERE Equipment_No=?""",t)
            print("get data", cursor.fetchall())
            print("Failed to insert data into sqlite table: ", error)

def py2sql(el):
    if el is None:
        return 'null'
    return el
def compare_equipID(conn,cursor,table_name,attr_list,ori_data):
    try:
        equip_no = ori_data[0]
        cursor.execute(f"""SELECT * FROM {table_name} WHERE Equipment_No=:equip_no""", {"equip_no":equip_no})
        fetched_data = cursor.fetchall()[0]
        fetched_data_tuple = tuple(map(py2sql, fetched_data))
        data_tuple = tuple(map(py2sql, ori_data))
        print("fetched_data_tuple[0]", fetched_data_tuple[0], "data_tuple[0]", data_tuple[0])
        same_ID_bool = (str(data_tuple[0]) == (fetched_data_tuple[0]))
        return [same_ID_bool, data_tuple, fetched_data_tuple]
    except sqlite3.Error as error:
        raise sqlite3.Error("Cannot search the compare query: ", error)
 


def update_data(conn, cursor,data_tuple,attr_list, table_name):
    try:
        equip_no = data_tuple[0]
        
        i=1
        set_statement=""
        while i < len(attr_list):
            if data_tuple[i] =='null':    
                set_statement += f"""{attr_list[i]} = {data_tuple[i]},"""
            else:
                set_statement += f"""{attr_list[i]} = '{data_tuple[i]}',"""
            i+=1
        set_statement = set_statement[:-1]
        cursor.execute(f"""UPDATE {table_name} SET {set_statement} WHERE Equipment_No=:equip_no""", {"equip_no":equip_no})
        conn.commit()
        # result = get_one_row_data(cursor, table_name, equip_no)
        # print("update data successfully: ", result)
    except sqlite3.Error as error:
        print("Cannot update table", error)


def get_one_row_data(cursor,table_name, equip_no):
    cursor.execute(f"""SELECT * FROM {table_name} WHERE Equipment_No=:equip_no""", {"equip_no":equip_no})
    q_result = cursor.fetchall()[0]
    return q_result
def get_data(conn,cursor,table_name):
    with conn:
        cursor.execute(f"""SELECT * FROM {table_name}""")
        print("getdata", cursor.fetchall())    


