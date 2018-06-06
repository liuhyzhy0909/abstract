# -*- coding: utf-8 -*-

import codecs,sys
import jieba
from numpy import *
from snownlp import SnowNLP
import math

reload(sys)
sys.setdefaultencoding('utf8')

def getData():
    fp = codecs.open('D:/news/auto_ab/5f127a35289a1235da2468e647710ff4.txt','r','utf-8')
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
    for i in range(1,size):
    #for i in range(size):
        text = text + DataList[i]+ '。'
    return text

#将文章划分为句子list
def getsentences(inputtext):
    re_text = inputtext.replace("。","/001").replace("？","/001").replace("!","/001").replace("；","/001")#.replace("“","/001").replace("”","/001")#.replace("(","/001").replace("）","/001")
    sents = re_text.split("/001")
    sentlist = [x.lstrip() for x in sents]
    sentlist_k = [x for x in sentlist if len(x) != 0]
    return sentlist_k

#获取文章的关键词
def getkeyword(inputtext):
    stn = SnowNLP(inputtext)
    keyw = stn.keywords(30)
    return set(keyw)

#将句子划分成词
def fenci(sentence):
    vocab = jieba.cut(sentence)
    vocabStr = "/".join(vocab)
    vocabList = vocabStr.split('/')
    vocabListend = [a for a in vocabList if len(a) != 0]
    return vocabListend

#统计每个句子中含有的关键词的个数
def intersectkeyws(sentList,keyset):
    s = len(sentList)
    tmp= zeros(s)
    for i in range(s):
        vocabListend = fenci(sentList[i])
        for j in range(len(vocabListend)):
            if vocabListend[j] in keyset:
                tmp[i] = tmp[i] + 1
    implist = dict(zip(sentList,tmp))
    return implist

#根据句子中含有关键词的个数计算句子的重要程度
def calimportity(sentList,keyset):
    intersectkeys = intersectkeyws(sentList,keyset)
    fordit = []
    result = []
    for v in intersectkeys.iteritems():
        fordit.append(v)
    for item in fordit:
        sen = item[0]
        inters = item[1]
        importity = inters*inters/len(fenci(sen))
        tuple1 = (sen,)
        tuple2 = (importity,)
        tu = tuple1 + tuple2
        result.append(tu)
    return dict(result)

#计算两个句子的相似度
def similarity(sent1,sent2):
    s1 = fenci( sent1)
    s2 = fenci(sent2)
    size1 = math.log(len(s1))
    size2 = math.log(len(s2))
    set1S = set(s1)
    set2S = set(s2)
    intersecti = len(set1S & set2S)
    similar = 0
    if size1+size2 != 0:
        similar = intersecti / (size1 + size2)
    else:
        similar = 0
    return similar

#将文章句子list进行减枝，对全文中的句子，计算句子两两之间的相似性，超过相似性阈值的句子只保留重要程度高的句子，保证句子list中的句子相似性程度很低
def decsentList(sents_point,p):
    sents_list = []
    del_list = []
    for item in sents_point.iteritems():
        sents_list.append(item)
    for i in range(len(sents_list)):
        for j in range(i+1,len(sents_list)):
            simi = similarity(sents_list[i][0],sents_list[j][0])
            if (simi > p and sents_list[i][1] > sents_list[j][1]):
                del_list.append(sents_list[j])
            elif (simi > p and sents_list[i][1] <= sents_list[j][1]):
                del_list.append(sents_list[i])
            else:
                del_list
    result = [x for x in sents_list if x not in del_list]
    return dict(result)

#确定摘要的压缩比
def getK(sents,reduce_rate):
    return int(len(sents)*reduce_rate)

#根据句子的重要程度，提取最重要的k个句子及句子对应的重要程度
def au_abstract(sen_point,k):
    sor_point = sorted(sen_point.iteritems(), key=lambda d:d[1], reverse = True)
    List = []
    point = []
    for i in range(len(sor_point)):
        item = sor_point[i]
        sents = item[0]
        po = item[1]
        List.append(sents)
        point.append(po)
    return point[:k],List[:k]

#根据句子重要程度，提取最不重要的k个句子，以便比较生成摘要的效果
def Nau_abstract(sen_point,k):
    sor_point = sorted(sen_point.iteritems(), key=lambda d:d[1], reverse = False)
    List = []
    point = []
    for i in range(len(sor_point)):
        item = sor_point[i]
        sents = item[0]
        po = item[1]
        List.append(sents)
        point.append(po)
    return point[:k],List[:k]

#将摘要按照原文的顺序输出
def re_sort_text(textlist,abstract):
    indexlist = []
    for i in abstract:
        s = textlist.index(i)
        indexlist.append(s)
    indexlist.sort()
    abs = []
    for i in range(len(indexlist)):
        ab = textlist[indexlist[i]]
        abs.append(ab)
    return abs

def main():
    aa = getData()
    title = getTitle(aa)
    text = getText(aa)
    sents = getsentences(text)
    if len(sents) == 0:
        print "本文内容为空，不能生成摘要"
    else:
        # k = getK(sents,0.2)
        k = 5
        ks = getkeyword(text)
        sen_point = calimportity(sents,ks)
        decpoint = decsentList(sen_point,2.0)
        point,abstractlist = au_abstract(sen_point,k)
        resort_abstract = re_sort_text(sents,abstractlist)
        pointend,abstractlistend = au_abstract(decpoint,k)
        not_point,not_abstractlist= Nau_abstract(sen_point,k)
        print "标题:"
        print "------------------------------------------------------------------------"
        print title
        print "------------------------------------------------------------------------"
        print "摘要"
        print "------------------------------------------------------------------------"
        for i in range(len(abstractlist)):
            print i+1,abstractlist[i]
        print "------------------------------------------------------------------------"
        print "摘要句子重要度："
        print "------------------------------------------------------------------------"
        for i in point:
            print i
        print "------------------------------------------------------------------------"
        print "按原文顺序输出摘要"
        print "------------------------------------------------------------------------"
        for i in range(len(resort_abstract)):
            print i + 1, resort_abstract[i]
        print "------------------------------------------------------------------------"
        if set(abstractlist) != set(abstractlistend):
            print "摘要中存在相似性很高的句子，修正后摘要"
            print "---------------------------------------------------------------------"
            for i in range(len(abstractlistend)):
                print i + 1, abstractlistend[i]
            print "---------------------------------------------------------------------"
            print "摘要句子重要度："
            print "---------------------------------------------------------------------"
            for i in pointend:
                print i
        print "------------------------------------------------------------------------"
        print "摘要top（-k）"
        print "------------------------------------------------------------------------"
        for i in range(len(not_abstractlist)):
            print i + 1, not_abstractlist[i]
        print "------------------------------------------------------------------------"
        for i in not_point:
            print i

main()