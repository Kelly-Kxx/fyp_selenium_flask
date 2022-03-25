import sqlite3
def Device_Excel_Table():
    table_name = "I_HKBCF_001_GF_AUS_PCW"
    conn = conn = sqlite3.connect("./website/database/HKBCF_001.db")
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