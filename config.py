#!/usr/bin/python3
# _*_coding:utf-8 _*_
# @Time　　:2020/6/24   14:19
# @Author　 : liwentong
#@ File　　  :config.py
import multiprocessing
import encodings.idna
PingHost=""
''' ssh-keygen 命令 '''
keygenCmd="ssh-keygen -q -t rsa -P '' -f ~/.ssh/id_rsa && echo yes || echo no"
''' 读取pub文件 '''
readPubCmd="test -f ~/.ssh/id_rsa.pub && cat ~/.ssh/id_rsa.pub || echo"
''' 查看pub文件是否存在 '''
testExistsCmd="test -f ~/.ssh/id_rsa.pub && echo yes || echo no"
''' 追加公钥至authorized_keys中'''
addKeyCmd="echo %s >> ~/.ssh/authorized_keys && echo yes || echo no"
'''进程数'''
Pnum=3