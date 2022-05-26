import sqlite3
def Device_Excel_Table(loc, sys, device):
    table_name = f"{loc}_{sys}_{device}"
    conn = conn = sqlite3.connect(f"./website/database/{loc}.db")
    cursor = conn.cursor()
   
    data_list = cursor.execute(f""" SELECT * 
                                    FROM {table_name}
                                    """)
    attr_list = []
    data = []
    for col in data_list.description:
        attr_list.append(col[0])
    for row in data_list:
        data.append(row)
    conn.commit()
    conn.close()
    return data, attr_list

def get_by_ID_from_table(loc, sys, device, id):
    table_name = f"{loc}_{sys}_{device}"
    conn = conn = sqlite3.connect(f"./website/database/{loc}.db")
    cursor = conn.cursor()
   
    data_list = cursor.execute(f""" SELECT * 
                                    FROM {table_name}
                                    WHERE Equipment_No = {id}""")
    attr_list = []
    data = []
    for col in data_list.description:
        attr_list.append(col[0])
    for row in data_list:
        data.append(row)
    conn.commit()
    conn.close()
    return data, attr_list



def get_arr(loc,sys=None):
    db_dir = "./website/database/"
    conn = sqlite3.connect(db_dir + '/'+ loc)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table'""")
    table_arr = cursor.fetchall()
    if sys is None:
        
        sys_arr = []
        for i in table_arr:
            spl = i[0].split('_')
            if spl[-2] not in sys_arr:
                sys_arr.append(spl[-2])
        return sys_arr
    else:
        device_arr = []
       
        for i in table_arr:
            spl = i[0].split('_')
            print(sys == spl[-2])
            if sys == spl[-2] and spl[-1] not in device_arr:
                device_arr.append(spl[-1])
        return device_arr
    # sys_arr, device_arr = [], []
    # for i in table_arr:
    #     spl = i[0].split('_')
    #     if spl[-2] not in sys_arr:
    #         sys_arr.append(spl[-2])
    #     if spl[-1] not in device_arr:
    #         device_arr.append(spl[-1])
    # if(sys_bool):
    #     return sys_arr
    # else:
    #     return device_arr