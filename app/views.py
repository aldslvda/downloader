from flask import render_template, request, redirect
from app import app
from forms import DownloaderForm
import time
import os
import sqlite3
@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'This is an ugly index page' } # fake user
    return render_template("index.html",
        title = 'Home',
        user = user)

@app.route('/downloader', methods = ['GET'])
def downloader(): 
    url = request.args.get('url')
    if 'http' not in url:
        return 'Not A Valid HTTP Url'
    filename = str(int(time.time()))[-7:]+'.mp4'
    
    cx = sqlite3.connect("videos.db")
    cu=cx.cursor()
    cu.execute('create table if not exists video (url text primary key, filename text)')
    cu.execute('select * from video where url="%s"'%url)
    cmdline = 'you-get -o /usr/share/nginx/html/ -O %s %s' %(filename, url)
    query_result = cu.fetchone()
    if query_result:
	url, vfile = query_result
	if os.path.exists('/usr/share/nginx/html/'+vfile):
            print 'File Exists !'
            return redirect('http://jp.aldslvda.tk:8080/'+vfile)
	else:
    	    print cmdline
    	    ret = os.system(cmdline)
    	    if ret:
	        return 'Download Error!'
            cu.execute('update video set filename="%s" where url="%s"'%(filename, url))
    else:
         print cmdline
         ret = os.system(cmdline)
         if ret:
             return 'Download Error'
         cu.execute('insert into video (url, filename) values ("%s","%s")'%(url, filename))
    cx.commit()
    cu.close()              
    #return 'Download Url: http://jp.aldslvda.tk:8080/'+filename
    return redirect('http://jp.aldslvda.tk:8080/'+filename)
