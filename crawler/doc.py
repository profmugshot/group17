class doc(object):
	def __init__(self, docID, title, html):
		self.docID = docID
		self.title = title
		self.html = html
	def setHTML(self, html): #gets the entire HTML doc
		self.html = html
	def getHTML(self):
		return self.html
	def getTitle(self):
		return self.title
	def getURL(self):
		return self.url	
	def getDocID(self):
		return self.docID
