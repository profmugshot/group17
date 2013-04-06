#!/usr/bin/python2.7
## Search

import jinja2 as jj
import os
import mod_locator
import cgi, cgitb
import MySQLdb
from bs4 import BeautifulSoup
import re
import itertools

##returns empty bucket of size "maxsize"
def bucket(maxsize):
    bucket = [0] * maxsize
    print "YOU MADE A BUCKET OF SIZE: " + str(maxsize) 
    return bucket
    
        
##returns back a bucket with all the new items added
def bucket_add(array,bucket):
    try:
        for item in array:
            bucket[item]=bucket[item]+1

    except:
        print 'none'
    #print "bucket at this point.. after adding..."
    #print bucket
    return bucket
    

def calculate_the_bucket(temp_array, maxsize):
    result = []

    #10%
    result.append( sum(temp_array[0:int(maxsize*0.1)]) )
    #20%
    result.append( sum(temp_array[int(maxsize*0.1):int(maxsize*0.2)]) )
    #30%
    result.append( sum(temp_array[int(maxsize*0.2):int(maxsize*0.3)]) )
    #40%
    result.append( sum(temp_array[int(maxsize*0.3):int(maxsize*0.4)]) )
    #50%
    result.append( sum(temp_array[int(maxsize*0.4):int(maxsize*0.5)]) )
    #60%
    result.append( sum(temp_array[int(maxsize*0.5):int(maxsize*0.6)]) )
    #70%
    result.append( sum(temp_array[int(maxsize*0.6):int(maxsize*0.7)]) )
    #80%
    result.append( sum(temp_array[int(maxsize*0.7):int(maxsize*0.8)]) )
    #90%
    result.append( sum(temp_array[int(maxsize*0.8):int(maxsize*0.9)]) )
    #100%
    result.append( sum(temp_array[int(maxsize*0.9):int(maxsize*1)]) )

    return result

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', unicode(element)):
        return False
    elif re.match('\n', unicode(element)):
        return False
    return True


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
query = querys[0].split(" ")

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

for docID in result:

    ##find the length of the docID
    sql='select html from docs where docID=%s;'
    cur.execute(sql, docID[0])
    db.commit()
    html_data = cur.fetchone()

    parsedPage = BeautifulSoup(html_data[0])
    text = parsedPage.findAll(text=True)
    page = filter(visible, text)
    page = [token.strip(' ').lower() for token in page]
    page = [token.split(' ') for token in page]
    page = list(itertools.chain.from_iterable(page))

    size_of_bucket = len(page)
    
    the_bucket = bucket(size_of_bucket)
    
    for aToken in query:
        print "FOR THIS DOCID: "
        print docID
        sql='select pos from indexterms where terms=%s AND docID=%s;'
        cur.execute(sql, (aToken,docID[0]))
        db.commit()
        jian_data = cur.fetchall()
        print "this is..." + aToken + " data."
        a = jian_data[0][0].split(',')
        JIAN = [int(y) for y in a]
        print JIAN

        bucket_add(JIAN,the_bucket)

    print "\n"
    print "running bucket for docID: " + str(docID)
    print calculate_the_bucket(the_bucket,size_of_bucket);
        #print "result for bucket is... " + str(bucket(JIAN, PEI))
    print "=======================================\n\n"

##
# Constructing variables to pass to HTML
var = {
    'title': 'CS456 G17 Jinja2 - '+querys[0],
    'heading': 'Jinja Demo',
    'query': querys[0],
    'results': result,
    'resultLen':len(result)
    }

##
# Render HTML...
template = env.get_template('search.html')
print template.render(var)


