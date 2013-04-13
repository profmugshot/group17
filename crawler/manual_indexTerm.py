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
                      passwd="ihave1cookie", # your password
                      db="storage") # name of the data base

######end db connection########

cur = db.cursor()
cur.execute('show tables like \'indexTerms\';')
db.commit()
if len(cur.fetchall())==0:
    print 'index term table does not exist, creating...'
    cur.execute( "create table indexTerms ("+
                 "terms VARCHAR(200) NOT NULL," +
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
    NumIndexedDocs = 0
    #cur.execute('select docID, html from docs;')
    #db.commit()

    #manually add docs that needs to be indexed
    profStr = '''http://www.cs.sfu.ca/people/faculty/gregbaker.html http://www.cs.sfu.ca/~ggbaker/ http://www.cs.sfu.ca/people/faculty/bradleybart.html http://www.cs.sfu.ca/~bbart/ http://www.cs.sfu.ca/people/faculty/petraberenbrink.html http://www.cs.sfu.ca/~petra/ http://www.cs.sfu.ca/people/faculty/binaybhattacharya.html http://www.cs.sfu.ca/~binay/ http://www.cs.sfu.ca/people/faculty/andreibulatov.html http://www.cs.sfu.ca/~abulatov/ http://www.cs.sfu.ca/people/faculty/robertdcameron.html http://www.cs.sfu.ca/~cameron/ http://www.cs.sfu.ca/people/faculty/dianacukierman.html http://www.cs.sfu.ca/people/faculty/ryandarcy.html http://www.cs.sfu.ca/%7Everonica/ http://www.cs.sfu.ca/people/faculty/veronicadahl1.html http://www.cs.sfu.ca/~veronica/ http://www.cs.sfu.ca/people/faculty/jamesdelgrande.html http://www.cs.sfu.ca/~jim/ http://www.cs.sfu.ca/people/faculty/tonydixon.html http://www.cs.sfu.ca/people/faculty/tobydonaldson.html http://www.cs.sfu.ca/people/faculty/markdrew.html http://www.cs.sfu.ca/~mark/ http://www.cs.sfu.ca/people/faculty/johnedgar.html http://www.cs.sfu.ca/people/faculty/fundaergun.html http://www.cs.sfu.ca/~funda/ http://www.cs.sfu.ca/people/faculty/martinester.html http://www.cs.sfu.ca/~ester/ http://www.cs.sfu.ca/people/faculty/mikeevans.html http://www.cs.sfu.ca/people/faculty/alexandrafedorova.html http://www.cs.sfu.ca/~fedorova/ http://www.cs.sfu.ca/people/faculty/brianfraser.html http://www.cs.sfu.ca/~bfraser/ http://www.cs.sfu.ca/people/faculty/brianfunt.html http://www.cs.sfu.ca/~funt/ http://www.cs.sfu.ca/people/faculty/uweglasser.html http://www.cs.sfu.ca/~glaesser/ http://www.cs.sfu.ca/people/faculty/QianpingGu.html http://www.cs.sfu.ca/~qgu/ http://www.cs.sfu.ca/people/faculty/louhafer.html http://www.cs.sfu.ca/~lou/ http://www.cs.sfu.ca/people/faculty/ghassanhamarneh.html http://www.cs.sfu.ca/~hamarneh/ http://www.cs.sfu.ca/people/faculty/mohamedhefeeda.html http://www.cs.sfu.ca/~mhefeeda/ http://www.cs.sfu.ca/people/faculty/pavolhell.html http://www.cs.sfu.ca/~pavol/ http://www.cs.sfu.ca/people/faculty/valentinekabanets.html http://www.cs.sfu.ca/~kabanets/ http://www.cs.sfu.ca/people/faculty/harindersinghkhangura.html http://www.cs.sfu.ca/~hskhangu/ http://www.cs.sfu.ca/people/faculty/arthurkirkpatrick.html http://www.cs.sfu.ca/~ted/ http://www.cs.sfu.ca/people/faculty/RameshKrishnamurti.html http://www.cs.sfu.ca/~ramesh/ http://www.cs.sfu.ca/people/faculty/annelavergne.html http://www.cs.sfu.ca/~alavergn/ http://www.cs.sfu.ca/people/faculty/ze-lianli.html http://www.cs.sfu.ca/~li/ http://www.cs.sfu.ca/people/faculty/arthurliestman.html http://www.cs.sfu.ca/~art/ http://www.cs.sfu.ca/people/faculty/jiangchuanliu.html http://www.cs.sfu.ca/~jcliu/ http://www.cs.sfu.ca/people/faculty/Wo-ShunLuk.html http://www.cs.sfu.ca/~woshun/ http://www.cs.sfu.ca/people/faculty/davidmitchell.html http://www.cs.sfu.ca/~mitchell/ http://www.cs.sfu.ca/people/faculty/gregmori.html http://www.cs.sfu.ca/~mori/ http://www.cs.sfu.ca/people/faculty/torstenmoller.html http://www.cs.sfu.ca/~torsten/ http://www.cs.sfu.ca/people/faculty/stevenpearce.html http://www.cs.sfu.ca/~stevenp/ http://www.cs.sfu.ca/people/faculty/jianpei.html http://www.cs.sfu.ca/~jpei/ http://www.cs.sfu.ca/people/faculty/JosephPeters.html http://www.cs.sfu.ca/~peters/ http://www.cs.sfu.ca/people/faculty/fredpopowich.html http://www.cs.sfu.ca/~popowich/ http://www.cs.sfu.ca/people/faculty/janiceregan.html http://www.cs.sfu.ca/~jregan/ http://www.cs.sfu.ca/people/faculty/cenkssahinalp.html http://www.cs.sfu.ca/~cenk/ http://www.cs.sfu.ca/people/faculty/anoopsarkar.html http://www.cs.sfu.ca/~anoop/ http://www.cs.sfu.ca/people/faculty/oliverschulte.html http://www.cs.sfu.ca/~oschulte/ http://www.cs.sfu.ca/people/faculty/thomasshermer.html http://www.cs.sfu.ca/~shermer/ http://www.cs.sfu.ca/people/Faculty/Profile/ashriram.html http://www.cs.sfu.ca/people/faculty/ArrvindhShriraman.html http://www.cs.sfu.ca/~ashriram/ http://www.cs.sfu.ca/people/Faculty/Profile/tamaras.html http://www.cs.sfu.ca/people/faculty/tamarasmyth.html http://www.cs.sfu.ca/~tamaras/ http://www.cs.sfu.ca/people/Faculty/Profile/tardos.html http://www.cs.sfu.ca/people/faculty/gabortardos.html http://www.cs.sfu.ca/~tardos/ http://www.cs.sfu.ca/people/Faculty/Profile/ter.html http://www.cs.sfu.ca/people/faculty/EugeniaTernovska.html http://www.cs.sfu.ca/~ter/ http://www.cs.sfu.ca/people/Faculty/Profile/vaughan.html http://www.cs.sfu.ca/people/faculty/richardvaughan.html http://www.cs.sfu.ca/~vaughan/ http://www.cs.sfu.ca/people/Faculty/Profile/wangk.html http://www.cs.sfu.ca/people/faculty/kewang.html http://www.cs.sfu.ca/~wangk/ http://www.cs.sfu.ca/people/faculty/kaywiese.html http://www.cs.sfu.ca/~wiese/ http://www.cs.sfu.ca/people/faculty/cynthiaxie.html http://www.cs.sfu.ca/people/Faculty/Profile/haoz.html http://www.cs.sfu.ca/people/faculty/richardzhang.html http://www.cs.sfu.ca/~haoz/'''

    indexedURLs = profStr.split(" ")
    #indexedURLs = ['http://www.cs.sfu.ca/~jpei']
    #for html in cur.fetchall(): #html returned is an array
    for urlLink in indexedURLs: #html returned is an array
	sql = 'select docID, html from docs where docID=%s'
	cur.execute(sql, urlLink)
	db.commit()
	html = cur.fetchone()
        NumIndexedDocs+=1
        print "\nURL[%s]: %s" %(NumIndexedDocs,html[0])
        NumIndexedTerms = 0
        soup = BeautifulSoup(html[1])
        text = soup.findAll(text=True)
        page = filter(visible, text) #an array containing all text
        page = clean(page) #formats all tokens from page
        pos = 0
##      debug=0;
        NumTotalTerms = len(page)
        print "\tTotal # terms: %s. Processing:" % NumTotalTerms
        
        for token in page:
            NumIndexedTerms+=1
            percent = float(NumIndexedTerms)/NumTotalTerms
            sys.stdout.write("\r\t%s (%.2f)" %(NumIndexedTerms,percent))
            sys.stdout.flush()
##            if debug>3:
##                break;
##            print token
            if len(token) > 200:
                print 'token too long ', token
                continue
            posList = [pos]
            sql = 'select pos from indexterms where docID=%s AND terms=%s'
            try:
                cur.execute(sql, (html[0], token))
                db.commit()
            except:
                print 'codec issue'
            #print token
            try:
                if (cur.fetchone() is None): #doesn't exist, adding
                    #print 'doesn\'t exist'
                    sql = 'insert into indexterms (terms, docID, pos) values (%s, %s, %s);'
                    cur.execute(sql, (token, html[0], str(pos)) )
                    db.commit()
                else:
                    #print 'does exist'
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
            except:
                print 'encoding issue', token
            pos = pos + 1
##            debug = debug + 1
##        break;

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
        page[i] = page[i].replace(']', '')
        page[i] = page[i].replace('[', '')
    return page
if __name__=="__main__":
    createIndexes()
