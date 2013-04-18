#!/usr/bin/python2.7
#!E:/Program Files (x86)/Python27/python.exe -u
## prof details

import jinja2 as jj
import os, sys
import mod_locator
import cgi, cgitb
import MySQLdb
from bs4 import BeautifulSoup
import re
import itertools
import operator
import namecard
DEBUG = 0
DO_RANK = 0
FREQ_COUNT=True
prof_bad_id = 0

#mysql connector
#--------------------------------------------
db = MySQLdb.connect(host="localhost", # your host, usually localhost
user="root", # your username
passwd="ihave1cookie", # your password
db="storage") # name of the data base
#--------------------------------------------
cur = db.cursor()


#============================================

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
querys = fs.getlist("id")
try:
    query = querys[0].split(" ")
except:
    if DEBUG: print "No Query"

if DEBUG: print query

##
# Constructing variables to pass to HTML
var = {
    'title': 'CS456 G17 Jinja2 - '+querys[0],
    'query': querys[0],
    }
##
# Render HTML...
template = env.get_template('headerNavBar.html')
print template.render(var)
sys.stdout.flush()
print env.get_template('searchProgress.html').render()
sys.stdout.flush()
###
#needs to clean the GET information, so that we only get int IDs

tokenDocList = []

sql = 'select * from professors where prof_id=%s;'
cur.execute(sql, querys[0])
db.commit()
tokenList = cur.fetchall()
tokenDocList.append(tokenList)

if(len(tokenList)<1):
    prof_name = ["jian pei"]
    prof_bad_id = 1
else:
    prof_name = str(tokenList[0][2])


sql = '''
    select subject,number,section,title,instructor from courses where instructor like %s;
    '''
cur.execute(sql, prof_name )
rows = cur.fetchall()
db.commit()

#freq count
if prof_bad_id:
    query = ["jian pei"]
else:
    query = str(tokenList[0][1]).split(" ")

result=[]
if query:
    for token in query:
        sql = 'select docID from indexterms where terms=%s;'
        cur.execute(sql, token)
        db.commit()
        tokenList = cur.fetchall()
        tokenDocList.append(tokenList)

    result = set(tokenDocList[0]).intersection(*tokenDocList)
    result = list(result)
    if DEBUG:
        print "Length of result: %s" %len(result)
        for i in result:
            print i

    #freq count
    if FREQ_COUNT:
        resultDic={}
        for token in query:
            #for url in result:
            sql = "select pos, docID from indexterms where terms=%s;"
            #cur.execute(sql, (token, url[0]))
            cur.execute(sql, (token))
            db.commit()
            rows2 = (cur.fetchall())

            pos = [freqIndex[0] for freqIndex in rows2] #get all positions of all indexes and store in pos
            posFreq = [len(freq.split(",")) for freq in pos] #split each positions into list and count them
            #print posFreq

            i=0
            for doc in rows2:
                try:
                    #if doc is in dictionary already, exception thrown if trying to access non-existing element
                    val = resultDic[doc[1]] #frequency for doc[1]
                    #resultDic.update( {doc[1]:posFreq[i]+val} ) #appends to ditionary
                    resultDic[doc[1]]=val+1

                except:
                    #if doc not in dictionary
                    resultDic.update( {doc[1]:posFreq[i]} ) #appends to ditionary
                i = i + 1
        outputResultDic = {}
        for docID in result:
            docID=docID[0]
            try: #if exist
                val = resultDic[docID]
                outputResultDic[docID] = val + 1
            except: #if not exist
                outputResultDic[docID] = 1
                #print 'something went wrong with freq ', docID
        result = sorted(outputResultDic.iteritems(), key=operator.itemgetter(1), reverse=True)

#print result

#print "this is the token list: " + str(tokenList[0][2])




##
# Constructing variables to pass to HTML	
var = {
    'title': 'CS456 G17 Jinja2 - '+querys[0],
    'query': querys[0],
    'prof': tokenDocList,
	'prof_bad_id': prof_bad_id,
    'rows': rows,
    'results': result,
    'tokenList': tokenList
    }

##
# Render HTML...
sys.stdout.flush()
template = env.get_template('prof_details.html')
print template.render(var)
print env.get_template('footer.html').render()
