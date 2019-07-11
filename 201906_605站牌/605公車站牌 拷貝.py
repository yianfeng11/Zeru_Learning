# -*- coding: utf-8 -*-
''' @author: ianfeng '''

import psycopg2
import pandas as pd
import json

conn = psycopg2.connect(database="TWIN_TAIPEI", 
                        user="postgres", 
                        password="ITS54290414", 
                        host="192.168.1.107", 
                        port="5432")
print("=== Opened database successfully ===")


#先利用路線名稱605找尋路線id
cur = conn.cursor()
sql = """select * from route_2019_3 
         where name_zh='605'"""
cur.execute(sql)
df_route = pd.read_sql(sql, conn)

#撈出路線id＝15514的站牌資料
sql = """select * from stop_2019_3 
         where route_id='15514'"""
cur.execute(sql)
df_stop = pd.read_sql(sql, conn)

#把站牌資料放進dict
rows = cur.fetchall()
stop_list = []
for row in rows:
    name_zh = row[2]
    lng = row[6]
    lat = row[7]
    stop_dict = {'name_zh':name_zh, 'lat':lat,'lng':lng}
    stop_list.append(stop_dict)
del(sql, row, rows, name_zh, lng, lat)

conn.close()

#轉成json
json_str =json.dumps(stop_list)


    
