import MySQLdb

#mysql connector
#--------------------------------------------
db = MySQLdb.connect(host="localhost", # your host, usually localhost
		user="root", # your username
		passwd="ihave1cookie", # your password
		db="storage") # name of the data base
#--------------------------------------------
cur = db.cursor()
form='drew computer vision professor'
query = form.split(' ')

tokenDocList = []
for token in query:
	sql = 'select docID from indexterms where terms=%s;'
	cur.execute(sql, token)
	db.commit()
	tokenList = cur.fetchall()
	tokenDocList.append(tokenList)

result = set(tokenDocList[0]).intersection(*tokenDocList)
result = list(result)
print len(result)
for i in result:
	print i
