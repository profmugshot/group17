from bs4 import BeautifulSoup
import sys, re
from urlparse import urljoin
import urllib2
import codecs
import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="", # your password
                     db="project_final") # name of the data base
cur = db.cursor()

seed = "http://portal.cs.sfu.ca/"
terms = ['1137','1134','1131','1127','1124','1121','1117','1111','1107','1104','1101','1097','1094','1091','1087','1084','1081','1077','1074','1071','1067','1064','1061','1057','1054','1051','1047']
#terms = ['1134']
for termID in terms:
    response = urllib2.urlopen('https://portal.cs.sfu.ca/outlines/'+str(termID))
    html = response.read()
    soup = BeautifulSoup(html)

    tabulka = soup.find("table", {"class" : "tablesorter"})

    records = [] # store all of the records in this list
    row_id = 0
    for row in tabulka.findAll('tr'):
        col = row.findAll('td')
        sys.stdout.write(termID+",")
        if col:
            subject = col[0].text.strip() 
            number = col[1].text.strip() 
            section = col[2].text.strip() 
            title = col[3].text.strip() 
            campus = col[4].text.strip() 
            instructor = re.sub(r"\s\s+", ';', col[5].text.strip())
            try:
                outline=urljoin(seed,col[6].a['href'])
            except:
                outline=""

            sql = '''
            insert into courses (
            subject, number, section, title, campus, instructor, outline,term)
             values (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            cur.execute(sql, (subject, number, section, title, campus, instructor, outline, termID) )
            db.commit()
            #print "values (%s, %s, %s, %s, %s, %s, %s, %s)"%(subject, number, section, title, campus, instructor, outline, termID) 
        #except:
         #   print "broke on row: " + str(row_id)

        row_id = row_id+1

    #fl = codecs.open('output_outlines.txt', 'wb', 'utf8')
    #line = ';'.join(records)
    #fl.write(line + u'\r\n')
    #fl.close()
