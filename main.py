#!/usr/bin/python3
# _*_coding:utf-8 _*_
# @Time　　:2020/6/24   11:46
# @Author　 : liwentong
#@ File　　  :main.py
import os
import sys
import threading
from gevent import monkey
monkey.patch_all()
import gevent
from myautossh import *
from config import *
Allresult={}
def read_macinfo(filepath):
    infoList=[]
    with open(filepath,'r') as f:
        for line in f.readlines():
            #一个空格切分数据
            lines=line.strip().split(' ')
            if len(lines)==4:
                infoList.append(lines)
    return infoList
#校验服务器情况
def conn_ssh(line):
    global Allresult
    aush = Myautossh(line[0], line[1], line[2], line[3])
    rec = aush.testPub()
    if len(rec)==0:
        if "no" not in Allresult.keys():
            Allresult["no"]=[]
            Allresult["no"].append(line[0])
        else:
            Allresult["no"].append(line[0])
    else:
        if "yes" not in Allresult.keys():
            Allresult["yes"] = {}
            Allresult["yes"][line[0]]=rec
        else:
            Allresult["yes"][line[0]]=rec
#携程配合多线程校验
def gevent_run(infoList):

    task_list=[]
    for line in infoList:
        task=gevent.spawn(conn_ssh,line)
        task_list.append(task)
    gevent.joinall(task_list)

#做互信
def addPublic(tcc):
    global Allresult
    ip=tcc[0]
    ic=tcc[1]
    try:
        myautossh=Myautossh(ip, ic[ip][0], ic[ip][1], ic[ip][2], Allresult["yes"])
        myautossh.addPub()
    except Exception as f:
        print(f)
#协程搭配多线程做户型
def gvent_run_add(ipList,ic):
    task_list=[]
    for line in ipList:
        task=gevent.spawn(addPublic,[line,ic])
        task_list.append(task)
    gevent.joinall(task_list)

def main():
    filepath='./1.txt'
    infoList=read_macinfo(filepath)

    #默认线程数为核心数
    step=int(len(infoList)/Pnum)
    if step==0:
        threading.Thread(target=gevent_run,args=(infoList,))
    else:
        tp=[]
        alist=[infoList[i:i+step] for i in range(0,len(infoList),step)]
        #print(alist)
        for linec in alist:
            t=threading.Thread(target=gevent_run,args=(linec,))
            t.start()
            tp.append(t)
        for i in tp:
            i.join()
    print("功能选项：1,1对N互信  2,N对N互信")
    #选出存活的已经获得公匙的服务器
    isActive=[i for i,value in Allresult["yes"].items()]
    isActiveInfo={}
    for i in infoList:
        if i[0] in isActive:
            isActiveInfo["%s"%i[0]]=i[1:]
    choice=input("输入你要做的功能选项:")
    if choice=='1':
        print("存活服务器列表：%s"%isActive)
        ipc=''
        while ipc!="break":
            ipc = input("输入你要做1对N互信的服务器ip(输入break退出):")
            if ipc in isActive:
                Myautossh(ipc,isActiveInfo[ipc][0],isActiveInfo[ipc][1],isActiveInfo[ipc][2],Allresult["yes"]).addPub()
            else:
                print("没有这个服务器" if ipc!='break' else '')
    elif choice=='2':
        #分任务
        step = int(len(isActive) / Pnum)
        print(step)
        if step == 0:
            t=threading.Thread(target=gvent_run_add, args=(isActive,isActiveInfo))
            t.start()
        else:
            tp=[]
            alist=[isActive[i:i+step] for i in range(0,len(isActive),step)]
            for line in alist:
                t=threading.Thread(target=gvent_run_add,args=(line,isActiveInfo))
                t.start()
                tp.append(t)
            for t in tp:
                t.join()

if __name__=='__main__':
    main()
