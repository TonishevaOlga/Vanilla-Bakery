# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:38:03 2021

@author: Дмитрий
"""

import sqlalchemy as adb
from sqlalchemy import MetaData, Table
import cx_Oracle as ora
import pandas as pd

#Функция подключения к БД в Oracle

def conn_to_db():
    
    l_user = 'Tonisheva_OV'
    l_pass = 'Olga1485'
    l_tns  = ora.makedsn('13.95.167.129', 1521, service_name = 'pdb1')
    
    try:
        l_conn_ora = adb.create_engine(r'oracle://{p_user}:{p_pass}@{p_tns}'.format(
                     p_user = l_user
                     , p_pass = l_pass
                     , p_tns = l_tns)
                     )
        print (l_conn_ora)
    except:
        print ('Возникла ошибка обращения к БД')        
    return l_conn_ora         

#Функция вставки данных в таблицу из файла Excel    

def insert_data():
    
    l_conn_ora = conn_to_db()
    l_meta = MetaData(l_conn_ora)
    l_meta.reflect()
    l_ord  = l_meta.tables['orders1']

#Начитываем данные из таблиц в файле Excel

    l_file_exc3 = pd.read_excel(r'C:\Users\79645\Desktop\Lab_DE\Vanilla Bakery.xlsx', sheet_name = 'Orders1')

#Приводим все данные с файла к списку
#Вставка данных в таблицу   

    l_list_ord = l_file_exc3.values.tolist() 
    for i in l_list_ord:
        l_ord.insert([l_ord.c.ord_id, l_ord.c.ord_date, l_ord.c.prod_id, l_ord.c.qty, l_ord.c.cust_id]).values(
        ord_id = i[0], ord_date = i[1], prod_id = i[2], qty = i[3], cust_id = i[4]).execute()
        print(3)     

#Функция для запуска пакета 

def start_pkg():
        
    l_conn_ora = conn_to_db()
    l_meta = MetaData(l_conn_ora)
    

    l_sql_exec = l_conn_ora.connect()
    l_conn_ora.execute(adb.text('BEGIN pkg_project.make_final_aggr_ord_summ_f; END;'))
    l_conn_ora.execute(adb.text('BEGIN pkg_project.make_final_aggr_month; END;'))
    print('Done')
  
      
    
if __name__=='__main__':
    #conn_to_db()
    #insert_data()
    start_pkg()