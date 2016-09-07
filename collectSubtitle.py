import os
import os.path
from common import *
import codecs
from zhtools.langconv import *
from zhtools.zh_wiki import *

class subtitleCollect:
	def __init__(self):
		self.postfixMap = {
		'.ass' : self.parserAss,
		'.srt' : self.passSrt,
		'.ssa' : self.parserAss
		}
		self.punctuationSet = set('~`!@#$%^&*()_-+=:;\"\'|\\<,>.?/~·！@#￥%……&*（）——-+=；：‘“”’|、《，》。？  ')
		self.engSetLower = set('qazxswedcvfrtgbnhyujmkilop')
		self.engSetUpper = set('QAZXSWEDCVFRTGBNHYUJMKIOLP')
		self.convert = Converter('zh-hans')

	def checkStringValid(self,line):
		return True
		if not line or (0 == len(line)):
			return False

		fpos = 0
		if len(line) >= 3:
			epos = len(line) - 3
		else:
			epos = 0	
		mpos = epos // 2
		checkList = [line[fpos]]
		if fpos != mpos:
			checkList.append(line[mpos])
		if mpos != epos:
			checkList.append(line[epos])

		for c in checkList:
			if (False == c.isdigit()) and (False == (c in self.engSetLower)) and (False == (c in self.engSetUpper)) and (False == (c in zh2Hant)) and (False == (c in self.punctuationSet)):
				return False

		return True			
			

	def parser(self,subtitleDir,outputFile):
		if not subtitleDir or not len(subtitleDir):
			return

		if not outputFile or not len(outputFile):
			return

		subtitleDir = appendBackslash(subtitleDir)	
		outFile = codecs.open(outputFile,'a','utf-16')
		if not outFile:
			return
		for parentDir,dirNames,fileNames in os.walk(subtitleDir):
			for fileName in fileNames:
				if len(fileName) <= 4:
					continue
				postfix = fileName[len(fileName) - 4:].lower()
				if False == (postfix in self.postfixMap):
					continue

				fullFilePath = os.path.join(subtitleDir,fileName)
				encode = getFileEncode(fullFilePath)
				valid = True
				try:
					file = codecs.open(fullFilePath,'r',encode)
				except:
					valid = False
				if False == valid:
					continue	
				subTitleList = self.postfixMap[postfix](file)
				file.close()
				for subtitle in subTitleList:
					rnPos = subtitle.find('\\N')
					if rnPos != -1:
						subtitle = subtitle[:rnPos]
					if(subtitle.find('}') != -1) or (subtitle.find('-=') != -1):
						continue
					subtitle = self.convert.convert(subtitle)
					subtitle = subtitle.replace('- ','')
					subtitle = subtitle.replace('<i>','')
					subtitle = subtitle.replace('</i>','')
					pos1 = subtitle.find('<')
					if pos1 != -1:
						pos2 = subtitle.find('>',pos1)
						if pos2 != -1:
							subtitle = subtitle[pos2 + 1:]
							if len(subtitle) == 0:
								continue
					pos1 = subtitle.find('[')
					if pos1 != -1:
						pos2 = subtitle.find(']',pos1)
						if pos2 != -1:
							subtitle = subtitle[pos2 + 1:]
							if len(subtitle) == 0:
								continue
					if self.checkStringValid(subtitle) == False:
						continue									
					outFile.write(subtitle)

		outFile.close()		

	def parserAss(self,file):
		if not file:
			return []
		tmpList = []
		startParser = False
		commaNum = 0
		while True:
			try:
				line = file.readline()
			except:
				return tmpList
			if len(line) == 0:
				return tmpList	
			if not startParser and (line == '[Events]\r\n'):
				try:
					line = file.readline()
				except:
					return tmpList
				while True:
					pos = line.find(',')
					if pos != -1:
						line = line[pos + 1:]
						commaNum += 1
						continue
					break	
				startParser = True
				continue
			elif not startParser:
				continue
			valid = True	
			for i in range(0,commaNum):
				pos = line.find(',')
				if -1 == pos:
					valid = False
					break
				line = line[pos + 1:]	
			if not valid:
				continue
			if line.find('Subindex build by Linnet') != -1:
				x = '123'		
			tmpList.append(line)

		return tmpList
			
	def passSrt(self,file):
		tmpList = []
		if not file:
			return tmpList
		while True:
			try:
				line = file.readline()
			except:
				return tmpList	
			if len(line) == 0:
				break	
			if line.find(' --> ') == -1:
				continue
			try:
				line = file.readline()
			except:
				continue
			if line.find('Subindex build by Linnet') != -1:
				x = '123'			
			tmpList.append(line)

		return tmpList				
