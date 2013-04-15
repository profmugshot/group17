import urllib2
from bs4 import BeautifulSoup
import sys, re
from urlparse import urljoin
import MySQLdb
debug = 0

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
    text_img =  i.find_all("div", {"class":"image"})[0]
    info_block = i.find_all("div", {"class":"text"})[0]
    #print text_img.img['src']
    print "<div class='member'>"
    
    print "<img src='"+urljoin(seed, text_img.img['src'])+"'/>"
    print info_block.h4 or info_block.h3
    all_a =  info_block.find_all("a")
    all_p =  info_block.find_all("p")
    print all_p[0]
    prof_name = ""
    rx = re.compile('\W+')
    try:
        if info_block.h4:
            prof_name=rx.sub('%',info_block.h4.text.split(",")[0]).strip()
        
    except:
        if debug: print "some professor has a broken<h4> name"

    try:
        if info_block.h3:
            prof_name=rx.sub('%',info_block.h3.text.split(",")[0]).strip()
    except:
        if debug: print "NO NAME?"
    if debug: print "this is prof_name: " + prof_name
    sql = '''
            select subject,number,section,title,instructor from courses where instructor like %s;
            '''
    cur.execute(sql, prof_name )
    rows = cur.fetchall()
    db.commit()
    if len(rows)<1:
        cur.execute(sql, prof_name[0]+"%"+prof_name.split("%")[-1])
        rows = cur.fetchall()
        db.commit()
    if len(rows)<1:
        cur.execute(sql, "%"+prof_name.split("%")[-1])
        rows = cur.fetchall()
        db.commit()

    print "<table cellspaceing='0'>"
    
    ###
    ##table header
    print "<tr><th>Subject</th><th>Number</th><th>Section</th><th>Title</th><th>Instructor</th></tr>"
    for row in rows:
        print "<tr class='even'>"
        #print "taught: " + str(row)
        print "<td>" + row[0] +"</td><td>" + row[1] +"</td><td>" + row[2] +"</td><td>" + row[3] +"</td><td>" + row[4] +"</td>"
        print "</tr>"
    print "</table>"

    for j in all_a:
        #j.get('href')=urljoin(seed, j.get('href'))
        #print j
        try:
            print "<a href='"+urljoin(seed, j.get('href'))+"' />"+j.string+"</a>"
        except:
            print ""
    print '\n'
    print "</div>"





