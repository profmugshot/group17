import urllib, urllister, weather_lister
sock = urllib.urlopen("http://www.cs.sfu.ca/people/faculty.html")
wsource = sock.read()
parser = urllister.URLLister()
parser2 = weather_lister.weatherParser()
parser2.feed(wsource)
parser.feed(wsource)
parser2.close()
sock.close()
parser.close()
#print wsource
#for url in parser.urls: print url
