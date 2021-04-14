# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:05:08 2021

@author: Дмитрий
"""

import sqlalchemy as adb
from sqlalchemy import MetaData, Table
import cx_Oracle as ora
import pandas as pd

#Подключение к БД в Oracle

l_user = 'Tonisheva_OV'
l_pass = 'Olga1485'
l_tns  = ora.makedsn('13.95.167.129', 1521, service_name = 'pdb1')

l_conn_ora = adb.create_engine(r'oracle://{p_user}:{p_pass}@{p_tns}'.format(
    p_user = l_user
    , p_pass = l_pass
    , p_tns = l_tns)
    )

print (l_conn_ora)

l_meta = MetaData(l_conn_ora)
l_meta.reflect()

#Переменные для вставки данных в таблицы в Oracle

l_prod = l_meta.tables['products1']
l_cust = l_meta.tables['customers1']
l_ord  = l_meta.tables['orders1']

#Начитываем данные из таблиц в файле Excel

l_file_exc1 = pd.read_excel(r'C:\Users\Дмитрий\Desktop\Lab_DE\Vanilla Bakery.xlsx', sheet_name = 'Products')
l_file_exc2 = pd.read_excel(r'C:\Users\Дмитрий\Desktop\Lab_DE\Vanilla Bakery.xlsx', sheet_name = 'Customers')
l_file_exc3 = pd.read_excel(r'C:\Users\Дмитрий\Desktop\Lab_DE\Vanilla Bakery.xlsx', sheet_name = 'Orders1')

#Приводим все данные с файла к списку
#Вставка данных в таблицу

l_list_prod = l_file_exc1.values.tolist() 
for i in l_list_prod:
    l_prod.insert([l_prod.c.prod_id, l_prod.c.prod_name, l_prod.c.price]).values(
        prod_id = i[0], prod_name = i[1], price = i[2]).execute()
    print(1)    #контроль вставки строк

l_list_cust = l_file_exc2.values.tolist() 
for i in l_list_cust:
    l_cust.insert([l_cust.c.cust_id, l_cust.c.last_n, l_cust.c.first_n, l_cust.c.mail, l_cust.c.district]).values(
        cust_id = i[0], last_n = i[1], first_n = i[2], mail = i[3], district = i[4]).execute()
    print(2)    

l_list_ord = l_file_exc3.values.tolist() 
for i in l_list_ord:
    l_ord.insert([l_ord.c.ord_id, l_ord.c.ord_date, l_ord.c.prod_id, l_ord.c.qty, l_ord.c.cust_id]).values(
        ord_id = i[0], ord_date = i[1], prod_id = i[2], qty = i[3], cust_id = i[4]).execute()
    print(3) 




