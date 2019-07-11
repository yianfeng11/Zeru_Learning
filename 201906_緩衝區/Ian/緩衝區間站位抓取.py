#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import psycopg2
import sys

#df
df = pd.read_csv('/Users/ianfeng/Desktop/test.csv')

#df1
conn = None
try:
    conn = psycopg2.connect(dbname = "TWIN_TAIPEI",
                           user = "postgres",
                           password = "ITS54290414",
                           host = "192.168.1.107",
                           port = "5432")
    sql = """SELECT * 
             FROM stop_2019_6 
             ORDER BY goback, seq_no"""
    df1 = pd.read_sql(sql, conn)
    print('df1')
    print(df1)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)
finally:
    if conn:
        conn.close()
        print("----- PostgreSQL connection is closed -----")
del(sql)
df1[['id']] = df1[['id']].astype(int)
df1[['route_id']] = df1[['route_id']].astype(int)
df1.info()

#df2
df2List = []
for i in range(2):
    a = df1[(df1['name_zh'] == df.loc[i, "0起"]) & (df1['goback'] == "0") & (df1['route_id'] == df.loc[i, 'id'])]['id'].values
    b = df1[(df1['name_zh'] == df.loc[i, "0迄"]) & (df1['goback'] == "0") & (df1['route_id'] == df.loc[i, 'id'])]['id'].values
    df2 = df1[(df1['route_id'] == df.loc[i, 'id'])
                & (df1['goback'] == "0")
                & ((df1['id'] >= a[0]) & (df1['id'] <= b[0]))]
    df2List.append(df2)
del(i, a, b)

#df3
df3List = []
for i in range(2):
    a = df1[(df1['name_zh'] == df.loc[i, "1起"]) & (df1['goback'] == "1") & (df1['route_id'] == df.loc[i, 'id'])]['id'].values
    b = df1[(df1['name_zh'] == df.loc[i, "1迄"]) & (df1['goback'] == "1") & (df1['route_id'] == df.loc[i, 'id'])]['id'].values
    df3 = df1[(df1['route_id'] == df.loc[i, 'id'])
                & (df1['goback'] == "1")
                & ((df1['id'] >= a[0]) & (df1['id'] <= b[0]))]
    df3List.append(df3)
del(i, a, b)

#all
df2_all = pd.DataFrame()
for j in range(2):
    c = df2List[j]
    df2_all = df2_all.append(c, ignore_index=True)
del(j, c)

df3_all = pd.DataFrame()
for j in range(2):
    c = df3List[j]
    df3_all = df3_all.append(c, ignore_index=True)
del(j, c)

df_all = df2_all.append(df3_all, ignore_index=True)
