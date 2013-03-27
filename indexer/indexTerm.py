import MySQLdb

##########db connection############
docDB={}
#mysql connector
db = MySQLdb.connect(host="localhost", # your host, usually localhost
		     user="root", # your username
		      passwd="test", # your password
		      db="storage") # name of the data base

######end db connection########

cur = db.cursor()
cur.execute('show tables like \'indexTerms\';')
db.commit()
if len(cur.fetchall()==0):
    print 'index term table does not exist, creating...'
    cur.execute( "create table indexTerms ("+
                 "terms VARCHAR(30) NOT NULL," +
                 "docID VARCHAR(100) NOT NULL PRIMARY KEY,"+
                 "pos VARCHAR(100) NOT NULL );"
                 );
    db.commit()
    cur.execute('SHOW DATABASES LIKE "indexTerms";')
    db.commit()
    assert len(cur.fetchall())!=0, 'table fail to create'

### parse from html doc ### 
