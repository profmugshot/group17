import urllib2
showProg=0

def read(url):
    return urllib2.urlopen(url).read()

## return:
##  file path
##  -1:bad url
##  -2:file larger than 1M
def save(url,path=""):
    file_name = url.split('/')[-1]
    try:
        u = urllib2.urlopen(url)
    except:
        return -1 #bad url
    f = open(path+file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    if file_size>1000000:
        return -2
    if showProg:
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        if showProg:
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
    f.close()
    return path+file_name