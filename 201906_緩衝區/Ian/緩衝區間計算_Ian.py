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


#緩衝區間篩選兩段票三段票路線
cur = conn.cursor()
sql = """select name_zh, segmentbufferzh 
               from route_2019_3 
               where datafrom='Taipei' 
               and ticketpricedescriptionzh<>'一段票' 
               and ticketpricedescriptionzh<>'依里程計費' 
               and ticketpricedescriptionzh<>'免費' 
               group by name_zh, segmentbufferzh"""
cur.execute(sql)
df = pd.read_sql(sql, conn)

#清洗站位名稱
buffer_station_list=[]
rows = cur.fetchall()
for row in rows:
    route_name=row[0]
    station=row[1].replace('(往)','',1).replace('(返)','',1).replace('(去程)','',5).replace('(返程)','',5).replace('去程:','',1).replace('往程:','',1).replace('返程:','',1).replace('(去)','',1).replace('(往程)','',1).replace('(返程)','',1).replace('-','－',10).replace(';','－',10).replace('、','－',10).replace('-','－',10).replace('、','－',5).replace(' ','－',10).replace('─','－',10).replace('~','－',10).replace('臺大)','臺大',10)
    ddd={'route_name':route_name,'station':station}
    buffer_station_list.append(ddd)
del(sql, row, rows, route_name, station, ddd)

#撈出站位之經緯度
sql = """select name, lon, lat 
          from stop_location_2019_3  
          where datafrom='Taipei'"""
cur.execute(sql)

rows = cur.fetchall()
station_dict = {}
for row in rows:
    name_zh=row[0];
    lng=row[1];
    lat=row[2];
    station_dict.setdefault(name_zh,{'lat':lat,'lng':lng})
del(sql, row, rows, name_zh, lng, lat)
conn.close()

#融合並轉換成json
for text in buffer_station_list:
    point_list=[]
    for text_station in text['station'].split('－'):#將每個站切割出來

        station = station_dict.get(text_station, "empty")##如果空值就放empty
        if(station!='empty'):
            point_list.append(station)
            
    text.update({'point_list': point_list})##將經緯度放進去
    
json_str =json.dumps(buffer_station_list)
    
        


    
