#!/usr/bin/python2.7
#!E:/Program Files (x86)/Python27/python.exe -u
## Search

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
##returns empty bucket of size "maxsize"
def bucket(maxsize):
    bucket = [0] * maxsize
    if DEBUG: print "YOU MADE A BUCKET OF SIZE: " + str(maxsize)
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

    result.append( sum(temp_array[0:int(maxsize*0.1)]) )#10%
    result.append( sum(temp_array[int(maxsize*0.1):int(maxsize*0.2)]) )#20%
    result.append( sum(temp_array[int(maxsize*0.2):int(maxsize*0.3)]) )#30%
    result.append( sum(temp_array[int(maxsize*0.3):int(maxsize*0.4)]) )#40%
    result.append( sum(temp_array[int(maxsize*0.4):int(maxsize*0.5)]) )#50%
    result.append( sum(temp_array[int(maxsize*0.5):int(maxsize*0.6)]) )#60%
    result.append( sum(temp_array[int(maxsize*0.6):int(maxsize*0.7)]) )#70%
    result.append( sum(temp_array[int(maxsize*0.7):int(maxsize*0.8)]) )#80%
    result.append( sum(temp_array[int(maxsize*0.8):int(maxsize*0.9)]) )#90%
    result.append( sum(temp_array[int(maxsize*0.9):int(maxsize*1)]) )#100%

    return max(result)



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

cgitb.enable()
print "Content-type:text/html\r\n\r\n"

##
# Setting JinJa Env.
path=mod_locator.mod_path()
path=os.path.dirname(path)
env = jj.Environment(loader=jj.FileSystemLoader(path+'/template'))

##
# Getting html form POST
query=['Jian','Pei']
fs = cgi.FieldStorage()
querys = fs.getlist("query")
try:
    query = querys[0].split(" ")
except:
    if DEBUG: print "No Query"
    querys=['Jian Pei']
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

##
# Name Card Search Results
namecards = namecard.generate_cards(query)

print env.get_template('searchProf.html').render(namecards=namecards)
sys.stdout.flush()

##
# Retrieving from database
tokenDocList = []
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

    if DO_RANK:
        rankLen = float(len(result))
        rankCnt = 0
        rankProgress=0.0
        resultDict={}
        for docID in result:
            rankCnt += 1
            print env.get_template('searchProgress.html').render(prog=rankCnt/rankLen*100)
            sys.stdout.flush()
            ##
            # find the length of the docID
            sql='select html from docs where docID=%s;'
            cur.execute(sql, docID[0])
            db.commit()
            html_data = cur.fetchone()

            ##
            # clean the parsed data
            try:
                page = html_data[0] #gets page
            except:
                continue
            parsedPage = BeautifulSoup(html_data[0])
            text = parsedPage.findAll(text=True)
            page = filter(visible, text)
            page = [token.strip(' ').lower() for token in page]
            page = [token.split(' ') for token in page]
            page = list(itertools.chain.from_iterable(page))

            size_of_bucket = len(page)

            the_bucket = bucket(size_of_bucket)

            print "</br>"
            #dictionary to store docID plus max bucket and sort
            for aToken in query:
                if DEBUG: print "FOR THIS DOCID: "
                if DEBUG: print docID
                sql='select pos from indexterms where terms=%s AND docID=%s;'
                cur.execute(sql, (aToken,docID[0]))
                db.commit()
                jian_data = cur.fetchall()
                if DEBUG: print "this is..." + aToken + " data."
                a = jian_data[0][0].split(',')
                JIAN = [int(y) for y in a]
                if DEBUG: print JIAN

                bucket_add(JIAN,the_bucket)
                if DEBUG:
                    print "\n"
                    print "running bucket for docID: " + str(docID)
                    print "SCORE: "
                    bucketScore = calculate_the_bucket(the_bucket,size_of_bucket);
                    resultDict.update({docID:bucketScore})
    	    else:
                    bucketScore = calculate_the_bucket(the_bucket,size_of_bucket);
                    resultDict.update({docID:bucketScore})

                #print "result for bucket is... " + str(bucket(JIAN, PEI))
                    print "</br>\n\n"

        #sort bucket results
        result = sorted(resultDict.iteritems(), key=operator.itemgetter(1), reverse=True)
        if DEBUG: print result
        result = [sortedLinks[0] for sortedLinks in result]
        #result = list(result)
    #freq count
    if FREQ_COUNT:
    	resultDic={}
    	for token in query:
    		#for url in result:
    		sql = "select pos, docID from indexterms where terms=%s;"
    		#cur.execute(sql, (token, url[0]))
    		cur.execute(sql, (token))
    		db.commit()
    		rows = (cur.fetchall())
    		pos = [freqIndex[0] for freqIndex in rows] #get all positions of all indexes and store in pos
    		posFreq = [len(freq.split(",")) for freq in pos] #split each positions into list and count them
    		#print posFreq

    		i=0
    		for doc in rows:
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

#print token
#print result

##
# Constructing variables to pass to HTML
var = {
    'title': 'CS456 G17 Jinja2 - '+querys[0],
    'query': querys[0],
    'results': result,
    'resultLen':len(result),
    'namecards': namecards
    }

##
# Render HTML...
sys.stdout.flush()
template = env.get_template('searchResult.html')
print template.render(var)
print env.get_template('footer.html').render()
