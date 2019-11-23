'''
@program: server.py

@description:

@author: doubleZ

@create: 2019/11/20
'''

# coding: utf-8
import eel
import os, base64
from base64 import b64decode
import sqlite3
from server.FullView import *


dirname = '../web/img/'

eel.init('../web')


def mkdir(newpath):
    path = "../web/img/"+newpath
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"
    else:
        print
        "---  There is this folder!  ---"



'''
将前端获取端Base64编码图片保存到本地
'''
@eel.expose
def get_origin_img(filename, img):
    '''处理数据(储存)'''
    with open(dirname + filename, 'wb') as f:
        # 将base64格式的数据解码成二进制数据并写入文件
        f.write(b64decode(img))
    print('图片' + filename + '已保存')


@eel.expose
def add_tag(UserDateLabel):
    conn = sqlite3.connect("../db/OneDay.db")
    # 创建游标
    c = conn.cursor()
    # 插入label
    c.execute("INSERT INTO tag (user_name,date,label) VALUES (?,?,?)",
              (UserDateLabel["user"], UserDateLabel["date"], UserDateLabel["label"]))
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()


@eel.expose
def read_panorama(UserDate):
    conn = sqlite3.connect("../db/OneDay.db")
    # 创建游标
    c = conn.cursor()
    # 读取数据
    c.execute("SELECT label FROM tag WHERE user_name = \'" + UserDate["user"] + "\'" + "AND date = \'" +UserDate["date"] + "\'")
    result1 = c.fetchall()
    c.close()
    # 创建游标
    c = conn.cursor()
    # 读取数据
    c.execute("SELECT description, path FROM panorama WHERE user_name = \'" + UserDate["user"] + "\'" + "AND date = \'" +UserDate["date"] + "\'")
    result2 = c.fetchone()
    result = {'path': result2[1], 'description': result2[0], 'label': result1}
    c.close()
    return result


@eel.expose
def add_panorama(UserDateImgnameImgsrcDesc):
    newpath = UserDateImgnameImgsrcDesc['user']+"/"+UserDateImgnameImgsrcDesc['date']
    mkdir(newpath)
    imgdata = base64.b64decode(UserDateImgnameImgsrcDesc["imgsrc"])
    file = open("../web/img/"+newpath+"/"+ UserDateImgnameImgsrcDesc['date'] + "."+ UserDateImgnameImgsrcDesc['imgname']
                .split('.')[1] , 'wb')
    file.write(imgdata)
    file.close()

    conn = sqlite3.connect("../db/OneDay.db")
    # 创建游标
    c = conn.cursor()
    # 插入UserDataImgnameImgsrc
    c.execute("INSERT INTO panorama (user_name,date,path,description) VALUES (?,?,?,?)",
              (UserDateImgnameImgsrcDesc["user"], UserDateImgnameImgsrcDesc["date"], newpath+"/"+
               UserDateImgnameImgsrcDesc['date'] + "."+ UserDateImgnameImgsrcDesc['imgname'].split('.')[1], UserDateImgnameImgsrcDesc["description"]))
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()


@eel.expose
def register(UserPwd):
    conn = sqlite3.connect("../db/OneDay.db")
    # 创建游标
    c = conn.cursor()
    c.execute("SELECT EXISTS(SELECT user_name FROM user WHERE user_name= \'"+UserPwd["username"]+"\')")
    state = {'state': False}
    if(c.fetchone()):
        return state
    # 插入User
    c.execute("INSERT INTO user (user_name,password) VALUES (?,?)",
              UserPwd["username"], UserPwd["password"])
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()
    state['state'] = True
    return state


@eel.expose
def login(UserPwd):
    conn = sqlite3.connect("../db/OneDay.db")
    # 创建游标
    c = conn.cursor()
    c.execute("SELECT EXISTS(SELECT user_name FROM user WHERE user_name= \'"+UserPwd["username"]+"\' AND password= \'"+
              UserPwd["password"] + "\')")
    state = {'state': False}
    if not c.fetchone():
        return state
    else:
        state['state'] = True
        return state


if __name__ == '__main__':
    eel.start('homepage.html')






