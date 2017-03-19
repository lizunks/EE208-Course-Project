#!/usr/bin/env python
import lucene
import chardet
import jieba
import sys

def run(command, searcher, analyzer):
    if command == '':
        return
    seg_list = jieba.cut(command)
    command = " ".join(jieba.cut(command))
    
    query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT, "charac",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs

    title = []
    url = []
    imgurl = []
    score = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        title.append(doc.get("title0"))
        url.append(doc.get("pUrl"))
        imgurl.append(doc.get("imgUrl"))
        score.append(doc.get("score"))

    query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT, "title",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        title.append(doc.get("title0"))
        url.append(doc.get("pUrl"))
        imgurl.append(doc.get("imgUrl"))
        score.append(doc.get("score"))

    resultInfo  = "%s total matching images." % len(title)  
    return resultInfo, title, url, imgurl, score

def func_pic(command):
    global vm_env
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR="graphIndex"
    directory = lucene.SimpleFSDirectory(lucene.File(STORE_DIR))
    searcher = lucene.IndexSearcher(directory, True)
    analyzer = lucene.SimpleAnalyzer(lucene.Version.LUCENE_CURRENT)
    title = []
    url = []
    imgurl = []
    score = []
    resultInfo, title, url, imgurl, score = run(command, searcher, analyzer)
    searcher.close()
    return resultInfo, title, url, imgurl, score



'''
    resultList =list()
    
    for scoreDoc in scoreDocs:
        rDict = dict()
        doc = searcher.doc(scoreDoc.doc)
        titlep = str(doc.get("title")).encode("gbk","ignore")
        rDict["title"] = titlep
        rDict["purl"]=doc.get("purl")
        rDict["imgUrl"]=doc.get("imgUrl")
        rDict["score"]=doc.get("score")
        # print 'path:', doc.get("path"), 'name:', doc.get("name"),'url:',doc.get("url"),'title:',titlep
        resultList.append(rDict)
    return resultInfo,resultList
    '''
