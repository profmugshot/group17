import urllib2
from bs4 import BeautifulSoup
import sys
from urlparse import urljoin
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
    

    for j in all_a:
        #j.get('href')=urljoin(seed, j.get('href'))
        #print j
        try:
            print "<a href='"+urljoin(seed, j.get('href'))+"' />"+j.string+"</a>"
        except:
            print ""
    print '\n'
    print "</div>"





