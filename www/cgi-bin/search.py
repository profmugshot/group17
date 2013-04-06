#!/usr/bin/python2.7
## Search

import jinja2 as jj
import os
import mod_locator
import cgi, cgitb

path=mod_locator.mod_path()
path=os.path.dirname(path)
env = jj.Environment(loader=jj.FileSystemLoader(path+'/template'))

cgitb.enable()

fs = cgi.FieldStorage()
querys = fs.getlist("query")
query = ""
query = query.join(querys)

var = {
    'title': 'CS456 G17 Jinja2 - '+query,
    'heading': 'Jinja Demo',
    'query': query
    }

template = env.get_template('search.html')
print "Content-type:text/html\r\n\r\n"
print template.render(var)
