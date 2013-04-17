#!/usr/bin/python2.7
#!E:/Program Files (x86)/Python27/python.exe -u

import jinja2 as jj
import os
import mod_locator

path=mod_locator.module_path()
env = jj.Environment(loader=jj.FileSystemLoader(path))

var = {
    'title': 'jinja2 template test',
    'heading': 'Jinja Demo',
    'names': ['iLly','Honda']
    }
template = env.get_template('template.html')
print  template.render(var)