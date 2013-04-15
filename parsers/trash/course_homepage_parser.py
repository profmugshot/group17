import urllib2
from bs4 import BeautifulSoup
import sys
from urlparse import urljoin
seed = "http://portal.cs.sfu.ca/"
page = urllib2.urlopen("https://portal.cs.sfu.ca/outlines/")
soup = BeautifulSoup(page)

textimage = soup.find_all("tr", {"id":"highlight_row"})


for i in textimage:
    i = i.replace("<br>", "")
    i = i.replace("</br>", "")
    text_img =  i.find_all("td", {"class":"highlighted"})
    course = text_img[1]
    course_name = text_img[3]
    try:
        outline = text_img[5].a["href"]
    except:
        print ""
    course_prof = text_img[4]
    outline = urljoin(seed, outline)
    #info_block = i.find_all("div", {"class":"text"})[0]
    #print text_img.img['src']
    #print "<img src='"+urljoin(seed, text_img.img['src'])+"'/>"
    #print info_block.h4 or info_block.h3
    #all_p =  info_block.find_all("p")

    #for j in all_p:
    #    print j
    #print '\n'
    #print text_img[0]
    print course
    print course_name
    print course_prof
    print outline

    print text_img
    
    print '========================='





