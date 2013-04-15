import urllib2
#from bs4 import BeautifulSoup
import sys, re
from urlparse import urljoin
import MySQLdb
debug = 0

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="", # your password
                     db="project_final") # name of the data base
cur = db.cursor()

def prof_db_lookup(prof_name):
    sql = '''
            select * from professors where prof_name like %s;
            '''
    cur.execute(sql, prof_name )
    rows = cur.fetchall()
    db.commit()
    return rows

def parse_query(query):
    prof_name = ""
    rx = re.compile('\W+')
    prof_name=rx.sub('%',query).strip()
    return "%"+prof_name+"%"

def generate_cards(query):
    if debug: print "I got query: " + query
    if debug: print "parsing query into tokens to look in database..."    
    if debug: print "adding %s between the queries to search better"
    prof_name = parse_query(query)
    if debug: print "result: " + prof_name
    
    if debug: print "looking up query in the database..."
    if debug: print "for each result fron db's professor, generate namecard..."
    return prof_db_lookup(prof_name)

def test(query='541'):
    data = generate_cards(query)
    print "Remember to turn on the debug to see steps."
    for entry in data:
        print entry[4]
        print
    
