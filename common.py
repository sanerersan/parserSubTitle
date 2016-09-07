import os

def appendBackslash(dirName):
	if not dirName or not len(dirName):
		return dirName

	if dirName[-1] != os.sep:
		dirName += os.sep

	return dirName		

def getFileEncode(fileName):
	file = open(fileName,'rb')
	if not file:
		return 'ascii'

	preBytes = file.read(2)
	if preBytes and (len(preBytes) == 2):
		if(0xFF == preBytes[0]) and (0xFE == preBytes[1]):
			return 'utf-16'
		elif (0xEF == preBytes[0]) and (0xBB == preBytes[1]):
			return 'utf-8'	
	file.close()
	return 'ascii'