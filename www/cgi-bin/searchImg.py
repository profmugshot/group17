#!/usr/bin/python2.7
#!E:/Program Files (x86)/Python27/python.exe -u

## libary are prepared as:
## faceRec_init.py : prepare a folder of pictures to subfolder(picName). faces crop/rotate by eye
## faceRec_lbphYML.py : train data from above folder and save to face-lbph.yml, save name to csv
## faceRec_lbph.py : load trained yml and predict image (need to be prepared first)
## faceRec_rec.ph : prepare image like faceinit and call faceRec-lbph.py

import jinja2 as jj
import os,sys
import mod_locator
import cgi, cgitb

path=mod_locator.mod_path()
pathRec=path+'/faceRec/'
sys.path.append(pathRec)
import faceRec_rec as rec
import URLopen as uo

path=os.path.dirname(path)
env = jj.Environment(loader=jj.FileSystemLoader(path+'/template'))
print "Content-type:text/html\r\n\r\n"

##
# Getting html form POST
cgitb.enable()
fs = cgi.FieldStorage()
link=""
var = {'title': 'CS456 G17 Jinja2'}

try:
    link = fs.getlist("imgURL")[0]
except:
    if 0:print "Unexpected error:", sys.exc_info()[0]

if not link or link[link.rfind('.')+1:] not in ['jpg','jpeg','png','gif']:
    ##
    # Constructing variables to pass to HTML
    print env.get_template('template.html').render(var)
    sys.stdout.write(env.get_template('imgSearch_typeError.html').render())
    sys.stdout.flush()
else:
    tmp=uo.save(link,pathRec+'tmp_download/')
    if tmp == -1:
        var['query'] = "The URL could not be succesfully downloaded..."
    else:
        label =rec.prepare_rec(tmp)
        if label is not None:
            var['query'] = label[1]
        else:
            var['query'] = "This image did not match anyone..."
    print env.get_template('template.html').render(var)
    print env.get_template('footer.html').render()