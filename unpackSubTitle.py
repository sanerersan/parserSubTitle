import os
import os.path
from common import *

def unpack(fileDir,outputDir):
	if not fileDir or not len(fileDir):
		return

	fileDir = appendBackslash(fileDir)
	outputDir = appendBackslash(outputDir)

	for parentDirs,dirNames,fileNames in os.walk(fileDir):
		for fileName in fileNames:
			if len(fileName) <= 4:
				continue
			postfix = fileName[len(fileName) - 4:].lower()
			if(postfix != '.zip') and (postfix != '.rar'):
				continue

			cmd = 'winrar.exe x -or -inul -ep ' + os.path.join(fileDir,fileName) + ' ' + outputDir
			os.system(cmd)