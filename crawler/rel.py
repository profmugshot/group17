def check(page):
	threshold = 10;
	#15 keywords
	keyWords = ['grad',
			'graduate',
			'students',
			'student',
			'research',
			'teaching',
			'contact',
			'degrees',
			'degree',
			'supervised',
			'supervise',
			'publications',
			'publication',
			'current research',
			'graduate students',
			'graduate student',
			'selected publications',
			'ph.d',
			'm.sc.']
	count = 0
	for token in keyWords:		
		if token in page:		
			count=count+1
	temp = float(100)*float((float(count)/float(len(keyWords))))	
	
	if temp>threshold:
		return True 
	else:
		return False 
