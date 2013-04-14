from bs4 import BeautifulSoup
import sys
from urlparse import urljoin
import urllib2
import codecs

seed = "http://portal.cs.sfu.ca/"
response = urllib2.urlopen('https://portal.cs.sfu.ca/outlines/1134/')
html = response.read()
soup = BeautifulSoup(html)

tabulka = soup.find("table", {"class" : "tablesorter"})

records = [] # store all of the records in this list
for row in tabulka.findAll('tr'):
    col = row.findAll('td')
    #outline_a = col.find_all("a")
    try:
        
        print col[0].text.strip() 
        print col[1].text.strip() 
        print col[2].text.strip() 
        print col[3].text.strip() 
        print col[4].text.strip() 
        print col[5].text.strip() 
        print urljoin(seed,col[6].a['href'])
    except:
        print "broke"
    print
    #prvy = col[1].string.strip()
    #druhy = col[1].string.strip()
    #record = '%s;%s' % (prvy, druhy) # store the record with a ';' between prvy and druhy
    #records.append(record)

fl = codecs.open('output_outlines.txt', 'wb', 'utf8')
line = ';'.join(records)
fl.write(line + u'\r\n')
fl.close()
