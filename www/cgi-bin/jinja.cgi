#!/usr/bin/python2.7
#!E:/Program Files (x86)/Python27/python.exe -u
import jinja2 as jj
import os
import mod_locator

path=mod_locator.mod_path()
path=os.path.dirname(path)
env = jj.Environment(loader=jj.FileSystemLoader(path+'/template'))

var = {
    'title': 'CS456 G17 Jinja2',
    'heading': 'Jinja Demo',
    'names': ['iLly','Honda']
    }
template = env.get_template('template.html')
print "Content-type:text/html\r\n"
print template.render(var)
