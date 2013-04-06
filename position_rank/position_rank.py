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

db = MySQLdb.connect(host="localhost", # your host, usually localhost
user="root", # your username
passwd="", # your password
db="storage") # name of the data base

cur = db.cursor()

tokens=['jian', 'pei']

for aToken in tokens:
    sql='select docid from indexterms where terms =\'jian\';'
    
arrayOne = [763,346,68,79]
arrayTwo = [7640,34,46,68,8008]

#print "running bucket"
#print "result for bucket is... " + str(bucket(arrayOne, arrayTwo))    

sql = 'select docID from indexterms where terms=\'jian\' and docID in (select docID from indexterms where terms=\'pei\');'

cur.execute(sql)
db.commit()
data = cur.fetchall()

for docID in data:

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
    
    for aToken in tokens:
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

    

