import urllib2
from bs4 import BeautifulSoup
import sys
from urlparse import urljoin
seed = "http://www.cs.sfu.ca/"
page = urllib2.urlopen("http://www.cs.sfu.ca/people/faculty.html")
soup = BeautifulSoup(page)

textimage = soup.find_all("div", {"class":"textimage section"})
#print len(textimage)

f=open('output.txt', 'w')
f.write('3132123')

for i in textimage:
    text_img =  i.find_all("div", {"class":"image"})[0]
    info_block = i.find_all("div", {"class":"text"})[0]
    #print text_img.img['src']
    print "<img src='"+urljoin(seed, text_img.img['src'])+"'/>"
    print info_block.h4 or info_block.h3
    all_p =  info_block.find_all("p")

    for j in all_p:
        print j
    print '\n'

    
##for i in textimage:
##    img_block = i.find_all("div", {"class":"text"})[0]
##    
##    f.write(img_block)
##    print img_block
##    print '\n'

f.close()




