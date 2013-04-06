#!/usr/bin/python2.7
## Search

import jinja2 as jj
import os
import mod_locator
import cgi, cgitb
import MySQLdb


#mysql connector
#--------------------------------------------
db = MySQLdb.connect(host="localhost", # your host, usually localhost
user="root", # your username
passwd="ihave1cookie", # your password
db="storage") # name of the data base
#--------------------------------------------
cur = db.cursor()


#============================================
DEBUG = 0

path=mod_locator.mod_path()
path=os.path.dirname(path)
env = jj.Environment(loader=jj.FileSystemLoader(path+'/template'))

cgitb.enable()

fs = cgi.FieldStorage()
querys = fs.getlist("query")
query = ",".join(querys)
form = query.replace(","," ")
query = query.strip(",")


tokenDocList = []
for token in query:
    sql = 'select docID from indexterms where terms=%s;'
    cur.execute(sql, token)
    db.commit()
    tokenList = cur.fetchall()
    tokenDocList.append(tokenList)

result = set(tokenDocList[0]).intersection(*tokenDocList)
result = list(result)

var = {
    'title': 'CS456 G17 Jinja2 - '+query,
    'heading': 'Jinja Demo',
    'query': form,
    'results': result,
    'resultLen':len(result)
    }

template = env.get_template('search.html')
print "Content-type:text/html\r\n\r\n"
print template.render(var)

if DEBUG: print query

print len(result)
for i in result:
print i
