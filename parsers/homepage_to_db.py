import urllib2
from bs4 import BeautifulSoup
import sys, re
from urlparse import urljoin
import MySQLdb
debug = 1

def removeNonAscii(s):return "".join(i for i in s if ord(i)<128)

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="", # your password
                     db="project_final") # name of the data base
cur = db.cursor()


seed = "http://www.cs.sfu.ca/"
sql_first = '''
    select prof_web_profile from professors
    '''
cur.execute(sql_first)
prof_web_profiles = cur.fetchall()
db.commit()

for prof_web_profile in prof_web_profiles:
    page = urllib2.urlopen(prof_web_profile[0])
    soup = BeautifulSoup(page)

    db_prof_image =""
    db_prof_name =""
    db_prof_contact=""
    db_prof_education=""
    db_prof_others=""
    db_prof_research=""

    image_block = soup.find_all("div", {"class":"parbase image section"})
    for item in image_block:
        db_prof_image = urljoin(seed, item.img['src'])
        
    title_block = soup.find_all("div", {"class": "title section"})
    for item in title_block:
        db_prof_name = item.h1.text

    summary_block = soup.find_all("div", {"class": "text parbase section"})
    rx = re.compile('\W+')
    for item in summary_block:
        see = item.find_all("h2")
        for content in see:
            if debug: print rx.sub('',content.text)
            try:
                if content.parent.contents[3]:
                    if rx.sub('',content.text) == "Education":
                        db_prof_education = removeNonAscii(content.parent.contents[3].text)
                    elif rx.sub('',content.text) == "Contact":
                        db_prof_contact = removeNonAscii(content.parent.contents[3].text).replace("\n",";").replace(";;","")
                    elif rx.sub('',content.text) == "Researchinterests":
                        db_prof_research = removeNonAscii(content.parent.contents[3].text)
                    else:
                        db_prof_others+=removeNonAscii(content.parent.text)
            except:
                print "you brokeee it D:"
        

    if debug:print "db_prof_image: " +db_prof_image 
    if debug:print "db_prof_name: "+removeNonAscii(db_prof_name)
    if debug:print "db_prof_contact: " + removeNonAscii(db_prof_contact)
    if debug:print "db_prof_education: " + removeNonAscii(db_prof_education)
    if debug:print "db_prof_research: " + removeNonAscii(db_prof_research)

    if debug:print "db_prof_others: " + removeNonAscii(db_prof_others)
    if debug:print

    db_prof_name = db_prof_name.replace(" " , "%")

    try:
        sql = '''
            update professors set
            prof_image_large=%s, prof_contact=%s, prof_education=%s, prof_research=%s, prof_others=%s
            where prof_name like %s;
            '''
        cur.execute(sql, (db_prof_image, db_prof_contact, db_prof_education, db_prof_research,db_prof_others, db_prof_name[0]+"%"+db_prof_name.split("%")[-1]))
    except:
        print "ERRORROOROROR:",sys.exc_info()[0]
    db.commit()






