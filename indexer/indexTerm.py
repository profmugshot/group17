import MySQLdb
import re
import sys
import itertools
from bs4 import BeautifulSoup

sys.setrecursionlimit(100000)
##########db connection############
#mysql connector
db = MySQLdb.connect(host="localhost", # your host, usually localhost
					 user="root", # your username
					  passwd="test", # your password
					  db="storage") # name of the data base

######end db connection########

cur = db.cursor()
cur.execute('show tables like \'indexTerms\';')
db.commit()
if len(cur.fetchall())==0:
	print 'index term table does not exist, creating...'
	cur.execute( "create table indexTerms ("+
				 "terms VARCHAR(30) NOT NULL," +
				 "docID VARCHAR(100) NOT NULL,"+
				 "pos VARCHAR(9999) NOT NULL );"
				 )
	db.commit()
	cur.execute( "alter table indexTerms add unique index(terms, docID);")
	db.commit()
	cur.execute('SHOW tables LIKE "indexTerms";')
	db.commit()
	assert len(cur.fetchall())!=0, 'table fail to create'

### parse from html doc ###

#filters only visible text in web browser
def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', unicode(element)):
		return False
	elif re.match('\n', unicode(element)):
		return False
	return True

def createIndexes():
	#cur.execute('select html from docs where docID=\"\'http://www.cs.sfu.ca/~mark\'\";')
	cur.execute('select docID, html from docs;')
	db.commit()
	for html in cur.fetchall(): #html returned is an array
		
		soup = BeautifulSoup(html[1])
		text = soup.findAll(text=True)
		page = filter(visible, text) #an array containing all text
		page = clean(page) #formats all tokens from page
		pos = 0
##		debug=0;
		for token in page:
##			if debug>3:
##				break;
			#print token
			posList = [pos]
			sql = 'select pos from indexterms where docID=%s AND terms=%s'
			cur.execute(sql, (html[0], token))
			db.commit()
			
			if (cur.fetchone() is None): #doesn't exist, adding
				print 'doesn\'t exist'
				sql = 'insert into indexterms (terms, docID, pos) values (%s, %s, %s);' 
				cur.execute(sql, (token, html[0], str(pos)) )
				db.commit()
			else:
				print 'does exist'
				#pos will be stored as '0,1,...,n'
				sql = 'select pos from indexterms where docID=%s AND terms=%s;'
				cur.execute(sql, (html[0],token))
				db.commit()
				
				posList = convertTupleToList(cur.fetchone())
				posList.append(pos)
				posList = convertListToStr(posList)
				sql = 'update indexterms set pos=%s where docID=%s AND terms=%s;'
				cur.execute(sql, (posList, html[0], token))
				db.commit()
			pos = pos + 1
##			debug = debug + 1
##		break;
			
#pulls POS tuple from DB, and then convert it into an integer list so new pos can be appended
#the data for pos is returned as a tuple ('0,..,n',) always, it expands the first element and nothing else
def convertTupleToList(pos):
        pos = pos[0].split(',')
        #pos = list(pos)
        #print pos
        pos = [int(strNum) for strNum in pos]
        return pos

def convertListToStr(pos):
        pos = [str(intNum) for intNum in pos]
        pos = ','.join(pos)
        return pos
        	
def clean(page):
	page = [token.strip(' ').lower() for token in page]
	page = [token.strip('\t') for token in page]
	page = [token.split(' ') for token in page]
	page = list(itertools.chain.from_iterable(page))
	
	#page = [re.sub(',*:*;*-*[\n][*]*[.]*[,]*', '', token) for token in page]
	#regex is an asshole and the three characters aren't being replaced. Fuck this shit
	for i in range(0, len(page)):
		page[i] = page[i].replace(',', '')
		page[i] = page[i].replace('.', '')
		page[i] = page[i].replace('`', '')
		page[i] = page[i].replace(':', '')
		page[i] = page[i].replace(';', '')
		page[i] = page[i].replace('\t', '')
		page[i] = page[i].replace('\n', '')
		page[i] = page[i].replace(')', '')
		page[i] = page[i].replace('(', '')
	return page
if __name__=="__main__":
	createIndexes()
