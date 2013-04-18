import urllib2
showProg=0
debug = 1
def read(url):
    return urllib2.urlopen(url).read()

## return:
##  file path
##  -1:bad url
##  -2:file larger than 1M
def save(url,path=""):
    file_name = url.split('/')[-1]
    if debug: print "got url:%s"%(url)
    if debug: print "filename:%s"%(file_name)
    try:
        u = urllib2.urlopen(url)
    except:
        return -1 #bad url
    f = open(path+file_name, 'wb')
    if debug: print "saveing to %s"%(path+file_name)
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
    if debug: print "done."
    f.close()
    return path+file_name