import sqlite3
from sqlite3 import Error
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql import func
from .db_requirement import item_requirement
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    

def create_table(conn, table_name, attr_list):
    try:
        statement = "Equipment_No text PRIMARY KEY ,"
        for attr in attr_list[1:]:
            if(attr[-1]=='_'):
                attr = attr[:-1]
            statement += f"{attr} text,"
        sql = f""" CREATE TABLE IF NOT EXISTS {table_name} ({statement[:-1]});"""
        #print(sql +"\n")
        c = conn.cursor()
        c.execute(sql)
       
    except Error as e:
        print(e)

def insert_one_row_data(conn,table_name,attr_list,str_data,ori_data,change_log): 
    try:
        insert_statement = "Equipment_No ,"
        for attr in attr_list[1:]:
            if(attr[-1]=='_'):
                attr = attr[:-1]
            insert_statement += f"{attr},"
        cursor = conn.cursor()
        insert_statement= insert_statement[:-1]
        insert_query = f"""INSERT INTO {table_name} ({insert_statement}) VALUES({str_data})"""
        # print("print",insert_query)
        cursor.execute(insert_query)
        print("after execute")
        conn.commit()
      
        result = get_one_row_data(cursor, table_name, ori_data[0])
        
        print("result",result)
        change_log.append({"type" : "inserted",
                            "table_name" : table_name, 
                            "attr_list" : attr_list,
                            "new_data" : result})
        return change_log
    except sqlite3.Error as error:
        cursor = conn.cursor()
        print("in error section")
        [same_ID_bool,data_tuple,fetched_data_tuple] = compare_equipID(conn,cursor,table_name,attr_list,ori_data)
        # print("same_ID", same_ID_bool, type(data_tuple[0]), type(fetched_data_tuple[0]))        
        if same_ID_bool: 

            if data_tuple != fetched_data_tuple:
                old_result = get_one_row_data(cursor, table_name, ori_data[0])
                
                update_data(conn,cursor,data_tuple,attr_list,table_name)
                new_result = get_one_row_data(cursor, table_name, ori_data[0])
                
                change_log.append({"type" : "updated",
                                    "table_name" : table_name,
                                    "attr_list" : attr_list,
                                    "ori_data" : old_result,
                                    "new_data" : new_result})
                return change_log
        else:
            t = (str(data_tuple[0]),)
            cursor.execute(f"""SELECT * FROM {table_name} WHERE Equipment_No=?""",t)
            result = cursor.fetchall()
            print("Failed to insert data into sqlite table: ", str(error))
            change_log.append({"type" : "error",
                                "error_message" : str(error),
                                "table_name" : table_name,    
                                "attr_list" : attr_list,
                                "ori_data" : result,
                                
            })
            return change_log
          
        
         

def py2sql(el):
    if el is None:
        return 'null'
    return el
def compare_equipID(conn,cursor,table_name,attr_list,ori_data):
    try:
        equip_no = ori_data[0]
        print("equip_no: ", equip_no)
        cursor.execute(f"""SELECT * FROM {table_name} WHERE Equipment_No=:equip_no""", {"equip_no":equip_no})
        
        fetched_data = cursor.fetchall()[0]
        print("fetchall2: ",fetched_data)
        fetched_data_tuple = tuple(map(py2sql, fetched_data))
        data_tuple = tuple(map(py2sql, ori_data))
        print("fetched_data_tuple",fetched_data_tuple, "data_tuple", data_tuple)
        print("fetched_data_tuple[0]", fetched_data_tuple[0], "data_tuple[0]", data_tuple[0])
        fetched_data_tuple = tuple(map(str, fetched_data_tuple))
        data_tuple= tuple(map(str, data_tuple))
        same_ID_bool = (data_tuple[0] == fetched_data_tuple[0])
        # if data_tuple[0] == "10901102":
        #         print(same_ID_bool, data_tuple==fetched_data_tuple )
        #         for d,e in zip(data_tuple, fetched_data_tuple):
        #             print("data tuple", d,e, d == e , type(d)==type(e))
              
            
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
                set_statement += f"""{attr_list[i]} = "{data_tuple[i]}","""
            i+=1
        set_statement = set_statement[:-1]
        print(set_statement)
        cursor.execute(f"""UPDATE {table_name} SET {set_statement} WHERE Equipment_No=:equip_no""", {"equip_no":equip_no})
        conn.commit()
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


