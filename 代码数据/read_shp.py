# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 10:26:59 2020

数据库实习
python读取shp文件
把点坐标等读进数据库

@author: shi'ying
"""

import pymssql
import shapefile as sf
import os

path="../地理数据/实习数据"

def conn():
    connect=pymssql.connect(
        'localhost:1433','sa','sy1999820.','COVID')
    if connect:
        print("连接成功！")
    return connect


def read_shp(file):
    shp=sf.Reader(os.path.join(path,file))
    record=sf.ShapeRecords(shp)
    #shapes=shp.shapes()
    fields=shp.fields
    
    val=[]
    typ=[]
    head=[]
    for i in record:
        val.append(i.record[0:])
        print(i.record[0:])
        typ.append(i.shape.shapeType)   #type=1表示点类型
        
        
    for i in fields:
        head.append(i[0])
    head.pop(0)                         #去掉FID
    return val,typ,head


def market_sql():
    market="market.shp"
    val,typ,head=read_shp(market)
    
    sql01="create table [WHU].[dbo].[market] (id integer primary key,name char(50),x float,y float,geometry geometry)"
    cursor.execute(sql01)
    conn.commit()
    
    for index in val:
        sql02="--insert into [WHU].[dbo].[market] (id,name,x,y,geometry) values({},'{}',{},{},geometry::STGeomFromText('POINT({} {})',4214))".format(index[0],index[1],index[2],index[3],index[2],index[3])
        cursor.execute(sql02)
        conn.commit()
    

def hospital_sql():
    hosptial="hospital.shp"
    val,typ,head=read_shp(hosptial)
    
    sql01="create table [WHU].[dbo].[hospital] (id integer primary key,name char(50),x float,y float,geometry geometry)"
    cursor.execute(sql01)
    conn.commit()
    
    for index in val:
        sql02="insert into [WHU].[dbo].[hospital] (id,name,x,y,geometry) values({},'{}',{},{},geometry::STGeomFromText('POINT({} {})',4214))".format(index[0],index[1],index[2],index[3],index[2],index[3])
        print(sql02)
        cursor.execute(sql02)
        conn.commit()
    

def road_sql():
    roadLine="roadLine.shp"
    shp=sf.Reader(os.path.join(path,roadLine))
    
    shapes=shp.shapes()           #所有线要素
    record=sf.ShapeRecords(shp)   #所有记录 
    shp.fields.pop(0)
    field=shp.fields              #所有title
    
    sql01="create table [WHU].[dbo].[road] (id integer primary key,name char(50),type char(50),length float,geometry geometry)"
    cursor.execute(sql01)
    conn.commit()
        
    for i in range(len(shapes)):
        rec_list=record[i].record[0:]
        shape_list=shapes[i].points
        ss=[]
        for index in shape_list:
            s=' '.join([str(i) for i in index])
            ss.append(s)
            xy=','.join(ss)
        #print(xy)
        sql02="insert into [WHU].[dbo].[road] (id,name,type,length,geometry) values({},'{}','{}',{},geometry::STGeomFromText('LINESTRING({})',4214))".format(rec_list[0],rec_list[1],rec_list[3],rec_list[4],xy)
        #print(sql02)
        cursor.execute(sql02)
        conn.commit()

def ground_sql():
    ground="ground.shp"
    shp=sf.Reader(os.path.join(path,ground))
    
    shapes=shp.shapes()
    record=sf.ShapeRecords(shp)
    shp.fields.pop(0)
    field=shp.fields
    
    sql01="create table [WHU].[dbo].[ground] (id integer primary key,name char(50),type char(50),length float,area float,geometry geometry)"
    cursor.execute(sql01)
    conn.commit()
    
    for i in range(len(shapes)):
        rec_list=record[i].record[0:]
        shape_list=shapes[i].points
        ss=[]
        for index in shape_list:
            s=' '.join([str(i) for i in index])
            ss.append(s)
            xy=','.join(ss)
        #print(xy)
        sql02="insert into [WHU].[dbo].[ground] (id,name,type,length,area,geometry) values({},'{}','{}',{},{},geometry::STGeomFromText('POLYGON(({}))',4214))".format(rec_list[0],rec_list[1],rec_list[2],rec_list[3],rec_list[4],xy)
        print(sql02)
        cursor.execute(sql02)
        conn.commit()

def build_sql():
    build="buildings.shp"
    shp=sf.Reader(os.path.join(path,build))
    
    shapes=shp.shapes()
    record=sf.ShapeRecords(shp)
    shp.fields.pop(0)
    field=shp.fields
    
    sql01="create table [WHU].[dbo].[building] (id integer primary key,name char(50),height integer,length float,area float,geometry geometry)"
    cursor.execute(sql01)
    conn.commit()
    
    for i in range(len(shapes)):
        rec_list=record[i].record[0:]
        shape_list=shapes[i].points
        ss=[]
        for index in shape_list:
            s=' '.join([str(i) for i in index])
            ss.append(s)
            xy=','.join(ss)
        #print(xy)
        sql02="insert into [WHU].[dbo].[building] (id,name,height,length,area,geometry) values({},'{}',{},{},{},geometry::STGeomFromText('POLYGON(({}))',4214))".format(rec_list[0],rec_list[1],rec_list[3],rec_list[4],rec_list[5],xy)
        print(sql02)
        cursor.execute(sql02)
        conn.commit()

  
if __name__=='__main__':
    conn=conn()
    #创建一个游标对象，python里的sql语句都要通过cursor来执行
    cursor=conn.cursor() 
    
    
    market_sql()
    hospital_sql()
    road_sql()
    ground_sql()
    build_sql()
    
    cursor.close()
    conn.close() 
