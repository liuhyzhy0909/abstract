#!/usr/bin/env python
#-*- coding:utf-8 -*-
import codecs,sys

from snownlp import SnowNLP

reload(sys)
sys.setdefaultencoding('utf8')

def getData():
    fp = codecs.open('D:/news/auto_ab/065b7007be26ac05e6d20763cd9e7d38.txt','r','utf-8')
    arr = []
    for lines in fp.readlines():
        lines = lines.replace("\n","")
        arr.append(lines)
    ar = [a for a in arr if len(a) != 0]
    return ar

def getTitle(DataList):
    return DataList[0]

def getText(DataList):
    size = len(DataList)
    text = ''''''
    #for i in range(size):
    for i in range(1,size):
        text = text + DataList[i]+ '。'
    return text

def abstract(k):
    aa = getData()
    title = getTitle(aa)
    text = getText(aa)
    s = SnowNLP(text)
    summary = s.summary(k)
    print "标题:"
    print "----------------------------------------------------------------"
    print title
    print "摘要"
    print "----------------------------------------------------------------"
    for i in range(len(summary)):
        print i+1,summary[i]
    print "----------------------------------------------------------------"


def main():
    abstract(5)

main()