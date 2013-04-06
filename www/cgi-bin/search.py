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
cgitb.enable()
print "Content-type:text/html\r\n\r\n"

##
# Setting JinJa Env.
path=mod_locator.mod_path()
path=os.path.dirname(path)
env = jj.Environment(loader=jj.FileSystemLoader(path+'/template'))

##
# Getting html form POST
fs = cgi.FieldStorage()
querys = fs.getlist("query")
query = ",".join(querys)
form = query.replace(","," ")
query = query.strip(",")

if DEBUG: print query

##
# Retrieving from database
tokenDocList = []
for token in query:
    sql = 'select docID from indexterms where terms=%s;'
    cur.execute(sql, token)
    db.commit()
    tokenList = cur.fetchall()
    tokenDocList.append(tokenList)

result = set(tokenDocList[0]).intersection(*tokenDocList)
result = list(result)

print len(result)
for i in result:
    print i

##
# Constructing variables to pass to HTML
var = {
    'title': 'CS456 G17 Jinja2 - '+query,
    'heading': 'Jinja Demo',
    'query': form,
    'results': result,
    'resultLen':len(result)
    }

##
# Render HTML...
template = env.get_template('search.html')
print template.render(var)


