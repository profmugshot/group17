import urllib2
from bs4 import BeautifulSoup
import sys, re
from urlparse import urljoin
import MySQLdb
debug = 0

def removeNonAscii(s):return "".join(i for i in s if ord(i)<128)

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="", # your password
                     db="project_final") # name of the data base
cur = db.cursor()


seed = "http://www.cs.sfu.ca/"
page = urllib2.urlopen("http://www.cs.sfu.ca/people/faculty.html")
soup = BeautifulSoup(page)

textimage = soup.find_all("div", {"class":"textimage section"})


for i in textimage:

    db_prof_image =""
    db_prof_name =""
    db_prof_course_search_name=""
    db_prof_web_profile=""
    db_prof_homepage=""

    
    text_img =  i.find_all("div", {"class":"image"})[0]
    info_block = i.find_all("div", {"class":"text"})[0]

    db_prof_image = urljoin(seed, text_img.img['src'])
    ###print info_block.h4 or info_block.h3
    all_a =  info_block.find_all("a")
    all_p =  info_block.find_all("p")
    ###print all_p[0]
    prof_name = ""
    rx = re.compile('\W+')
    try:
        if info_block.h4:
            prof_name=rx.sub('%',info_block.h4.text.split(",")[0]).strip()
            normal_prof_name = info_block.h4.text.split(",")[0]
        
    except:
        if debug: print "some professor has a broken<h4> name"

    try:
        if info_block.h3:
            prof_name=rx.sub('%',info_block.h3.text.split(",")[0]).strip()
            normal_prof_name = info_block.h3.text.split(",")[0]
    except:
        if debug: print "NO NAME?"
    if debug: print "this is prof_name: " + prof_name
    

    db_prof_name = normal_prof_name
    db_prof_course_search_name = prof_name


    for j in all_a:
        try:
            if j.get('href').split("/")[1] == "people":
                db_prof_web_profile = urljoin(seed, j.get('href'))
                tracker = 1
            else:
                db_prof_homepage = urljoin(seed, j.get('href'))
                tracker = 0
        except:
            if debug: print "something went wrong with the contact links"


    if debug:print "db_prof_image: " +db_prof_image 
    if debug:print "db_prof_name: "+removeNonAscii(db_prof_name)
    if debug:print "db_prof_course_search_name: " + db_prof_course_search_name
    if debug:print "db_prof_web_profile: " + db_prof_web_profile
    if debug:print "db_prof_homepage: " + db_prof_homepage
    if debug:print

    sql = '''
        insert into professors (
        prof_name, prof_course_search_name, prof_image,prof_image_large, prof_web_profile, prof_homepage, prof_contact, prof_education, prof_research, prof_others)
         values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
    cur.execute(sql, (removeNonAscii(db_prof_name), db_prof_course_search_name, db_prof_image, "#", db_prof_web_profile, db_prof_homepage, "Not Available","Not Available","Not Available","Not Available") )
    db.commit()






