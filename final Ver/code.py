# -*- coding: utf-8 -*-
import web
from web import form
import urllib2
import os
from lucene import *
from MySearcherG import *
from search import *

urls = (
    '/', 'index',
    '/t', 't',
    '/s', 's',
    '/p', 'p'
)

render = web.template.render('templates') # your templates

class index:
    def GET(self):
        return render.starter()

class t:
    def GET(self):
        return render.next()

    def POST(self):
        x = web.input(myfile={})
        print x.myfile.filename
        filedir = 'C:/Users/DELL-PC/Desktop/final Ver' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
            url,imgurl,description,rate = Search((x.myfile.filename))
        return render.picturez(len(url),description,url,imgurl,rate)

'''
class s:
    def GET(self):
        user_data = web.input()
        keyword = user_data.keyword
        title, url, surround = func(keyword)
        return render.website(keyword, title, url, surround)
        '''

class p:
    def GET(self):
        user_data = web.input()
        keyword = user_data.keyword
        resultInfo, title, url, imgurl, score = func_pic(keyword)
        return render.picture(keyword, resultInfo, title, url, imgurl, score)



if __name__ == "__main__":
    vm_env = initVM()
    app = web.application(urls, globals())
    app.run()

#经济



