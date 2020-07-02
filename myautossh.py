#!/usr/bin/python3
# _*_coding:utf-8 _*_
# @Time　　:2020/6/24   14:17
# @Author　 : liwentong
#@ File　　  :myautossh.py
import paramiko
import sys
import os
import socket
from config import *
class Myautossh(object):
    def __init__(self,ip,username,password,port,*args):
        self.ip=ip
        self.username=username
        self.password=password
        self.port=port
        self.result=''
        self.success=False
        self.server=paramiko.SSHClient()
        self.macInfoList='' if len(args)==0 else args[0]

    def checkHostExist(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip, int(self.port)))
            s.settimeout(2)
            self.success=True
        except Exception as f:
            self.success=False
    def check_pub(self):
        self.server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.server.connect(self.ip,int(self.port),self.username,self.password)
        stdin, stdout, stderr = self.server.exec_command(readPubCmd)
        pubresult=stdout.read().decode('utf-8').replace('\n','')
        if len(pubresult)>0:
            self.result=pubresult
        else:
            retry=0
            #尝试执行三次
            while retry<3:
                stdin,stdout,stderr=self.server.exec_command(keygenCmd)
                rec=stdout.read().decode('utf-8')
                if rec=="yes":
                    break
                retry+=1
            stdin,stdout,stderr=self.server.exec_command(readPubcmd)
            rec=stdout.read().decode('utf-8').replace('\n','')
            if len(rec)>0:
                self.result=rec
    #单增加公匙到
    def addPub(self):
        self.server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.server.connect(self.ip, int(self.port), self.username, self.password)
        for uip,pub in self.macInfoList.items():
            addcmd = addKeyCmd % (pub)
            stdin, stdout, stderr = self.server.exec_command(addcmd)
            if stdout.read().decode("utf-8").strip()=="yes":
                print("%s 对 %s 互信成功"%(uip,self.ip))
            else:
                print("%s 对 %s 互信失败"%(uip,self.ip))


    def testPub(self):
        self.checkHostExist()
        if self.success:
            self.check_pub()
        if len(self.result)!=0:
            return self.result
        else:
            return ''





