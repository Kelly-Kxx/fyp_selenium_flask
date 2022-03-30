import re
def location_requirement(excel_file):
    loc = excel_file.split('_')[1] #CSS_HKBCF-001_BR1102_20220315_054759_forida -> HKBCF-001
    loc = loc.replace('-','_') #HKBCF_001
    return loc

def attr_requirement(attr_list):
    for i in range(len(attr_list)):
        attr_list[i] = re.sub(r'(\(.*|\n*\)|(\.))', '',attr_list[i])  
        attr_list[i] = re.sub(r'-', '_',attr_list[i])
        attr_list[i] = re.sub(r'/', '_',attr_list[i])
        attr_list[i] = re.sub(r'&', '_',attr_list[i]) 
        attr_list[i] = re.sub(r' ', '_',attr_list[i])  
        attr_list[i] = re.sub(r'\n', '_',attr_list[i])  
    return attr_list

def table_name_initialization(loc, asset_code):
    table_name = loc + '_'
    for i,name in enumerate(asset_code):
        if(i==4 or i ==5):
            table_name += name +'_'
    table_name = table_name[:-1]
    return table_name

def item_requirement(item):
    item = str(item)
    item = item.replace("[",'')
    item= item.replace("]",'')
    item= item.replace("&",'')
    item = item.replace("None",'null')
    return item