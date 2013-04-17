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
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
    f.close()
    return path+file_name