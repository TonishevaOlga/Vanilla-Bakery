# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:38:03 2021

@author: Дмитрий
"""

import sqlalchemy as adb
from sqlalchemy import MetaData, Table
import cx_Oracle as ora

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
    start_pkg()