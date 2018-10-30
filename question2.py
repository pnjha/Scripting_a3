import os
import sys
import time
import re
import stat
from stat import *
from pathlib import Path
from datetime import datetime
    

def executeTouch(filePath):

	if os.path.isfile(filePath) == True:
		
		curTime =  int(round(time.time()))

		os.utime(filePath,(curTime,curTime))
	
	else:
		if os.path.isdir(filePath) == False:
			print("Its not a file nor folder")
			fileHandler = open(filePath,'w')
			fileHandler.close()
	
		else :
			print("> Its a directory")		

def executePWD():

	print(">",os.getcwd())

def executeCD(dirPath):
	if isinstance(dirPath,str):
		if dirPath == "~":
			dirPath = str(Path.home())
		try: 	
			os.chdir(dirPath)
			
		except FileNotFoundError: 
			print("> Invalid Path") 	
	else:
		print("> Invalid path")	

def executeGrep(pattern,filePath):
	try:
		pattern = re.compile(pattern)
		if os.path.isfile(filePath) == True:
			for line in open(filePath):
				if re.search(pattern,line):
					line = line.rstrip("\n")
					print("> ",line)

		else:
			print("> No such file exits")

	except FileNotFoundError:
		print("> Invalid path")		

def executeHead(commandList):

	lineCount = 10
	try: 
		if len(commandList) != 2 and commandList[1] == "-n":
			lineCount = int(commandList[2])
			filePath = commandList[3]
		else:
			filePath = commandList[1]	

		if lineCount <= 0:
			lineCount = 10	

		try:
			if os.path.isfile(filePath) == True:
				for line in open(filePath,"r"):
					line = line.rstrip('\n')
					if lineCount > 0:
						print("> ",line)
					else:
						break
					lineCount -= 1							
			else:
				print("> No such file exits")

		except UnicodeDecodeError:
			print("> Invalid file format")			
		except FileNotFoundError:
			print("> Invalid path")		
	except IndexError:
		print("> Invalid input")			

def executeTail(commandList):
	lineCount = 10
	try: 
		if len(commandList) != 2 and commandList[1] == "-n":
			lineCount = int(commandList[2])
			filePath = commandList[3]
		else:
			filePath = commandList[1]	

		if lineCount <= 0:
			lineCount = 10	

		lineList = []	

		try:
			if os.path.isfile(filePath) == True:
				for line in reversed(open(filePath).readlines()):
					if lineCount > 0:
						lineList.append(line.rstrip("\n"))
						lineCount -= 1
					else:
						break	
			else:
				print("> No such file exits")

			for line in reversed(lineList):
				print("> ",line)

		except UnicodeDecodeError:
			print("> Invalid file format")			
		except FileNotFoundError:
			print("> Invalid path")		
	except IndexError:
		print("> Invalid input")

def executeSed(commandList):

	try:
		if len(commandList) == 4:
			
			patternToReplace = commandList[1]
			patternToInsert = commandList[2]
			filePath = commandList[3]

			if os.path.isfile(filePath) == True:
				for line in open(filePath,"r"):
					line = line.rstrip('\n')

					patternToReplace = re.compile(patternToReplace)
					line = re.sub(patternToReplace, patternToInsert, line)
					
					print("> ",line)

			else:
				print("> No such file exits")

		elif len(commandList) == 5 and commandList[1] == "-i":	

			patternToReplace = commandList[2]
			patternToInsert = commandList[3]
			filePath = commandList[4]

			lineList = []

			if os.path.isfile(filePath) == True:
				for line in open(filePath,"r"):
					line = line.rstrip('\n')
					
					patternToReplace = re.compile(patternToReplace)
					line = re.sub(patternToReplace, patternToInsert, line)
					
					lineList.append(line)
					print("> ",line)

				file = open(filePath,"w")
				for line in lineList:
					file.write("%s\n" % line)	
				file.close()
	
			else:
				print("> No such file exits")			

	except UnicodeDecodeError:
		print("> Invalid file format")			
	
	except FileNotFoundError:
		print("> Invalid path")

	except IndexError:
		print("> Invalid input")	

def executeDiff(commandList):

	try:
		filePath1 = commandList[1]
		filePath2 = commandList[2]

		lineList1 = []
		lineList2 = []
		diffList = []

		if os.path.isfile(filePath1) == True and os.path.isfile(filePath2) == True:
			for line in open(filePath1):
				line = line.rstrip('\n')
				lineList1.append(line)

			for line in open(filePath2):
				line = line.rstrip('\n')
				lineList2.append(line)

			for item in lineList2:
				if item not in lineList1:
					diffList.append(item)

			diffList.append("......")			

			for item in lineList1:
				if item not in lineList2:
					diffList.append(item)

			flag = False	

			for item in diffList:
				
				if item == "......":
					flag = True

				if flag == True:	
					print("> ",item)
				else:
					print("< ",item)		

		else:
			print("> No such file exists")		

	except UnicodeDecodeError:
		print("> Invalid file format")			
	
	except FileNotFoundError:
		print("> Invalid path")

	except IndexError:
		print("> Invalid input")		

def executeLS(commandList):

	try:
		if len(commandList) == 1:
			filePath = str(os.getcwd())
			dirlist = os.listdir(filePath)
			for item in dirlist:
				print(item)

		elif len(commandList) == 2 and commandList[1] != "-l":

			dirlist = os.listdir(commandList[1])
			for item in dirlist:
				print(item)

		elif len(commandList) == 2 and commandList[1] == "-l":	
			try:
				dirEntries = os.scandir(os.getcwd())
				for entry in dirEntries:

					info = entry.stat()

					print(("-","d")[S_ISDIR(info[ST_MODE])], end="")
					print(("-","r")[bool(info[ST_MODE] & stat.S_IRUSR)], end="")
					print(("-","w")[bool(info[ST_MODE] & stat.S_IWUSR)], end="")
					print(("-","x")[bool(info[ST_MODE] & stat.S_IXUSR)], end="")
					print(("-","r")[bool(info[ST_MODE] & stat.S_IRGRP)], end="")
					print(("-","w")[bool(info[ST_MODE] & stat.S_IWGRP)], end="")
					print(("-","x")[bool(info[ST_MODE] & stat.S_IXGRP)], end="")
					print(("-","r")[bool(info[ST_MODE] & stat.S_IROTH)], end="")
					print(("-","w")[bool(info[ST_MODE] & stat.S_IWOTH)], end="")
					print(("-","x")[bool(info[ST_MODE] & stat.S_IXOTH)], end="")

					print("\t",info[ST_SIZE],"\t", entry.name, end="")
					print ("\t\t\t", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info[ST_MTIME])))

			except OSError:
				print("Unable to read the given directory..")

		elif len(commandList) == 3 and commandList[1] == "-l":	
			try:
				dirEntries = os.scandir(commandList[2])
				for entry in dirEntries:

					info = entry.stat()

					print(("-","d")[S_ISDIR(info[ST_MODE])], end="")
					print(("-","r")[bool(info[ST_MODE] & stat.S_IRUSR)], end="")
					print(("-","w")[bool(info[ST_MODE] & stat.S_IWUSR)], end="")
					print(("-","x")[bool(info[ST_MODE] & stat.S_IXUSR)], end="")
					print(("-","r")[bool(info[ST_MODE] & stat.S_IRGRP)], end="")
					print(("-","w")[bool(info[ST_MODE] & stat.S_IWGRP)], end="")
					print(("-","x")[bool(info[ST_MODE] & stat.S_IXGRP)], end="")
					print(("-","r")[bool(info[ST_MODE] & stat.S_IROTH)], end="")
					print(("-","w")[bool(info[ST_MODE] & stat.S_IWOTH)], end="")
					print(("-","x")[bool(info[ST_MODE] & stat.S_IXOTH)], end="")

					print("\t",info[ST_SIZE],"\t", entry.name, end="")
					print ("\t\t", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info[ST_MTIME])))

			except OSError:
				print("Unable to read the given directory..")			

		else:
			print("Invalid Input")

	except IndexError:
		print("> Invalid input")

def executeTR(commandList):
	pass


def main():
	while True:

		print(">", end =" ")
		userInput = input()
		cmdList = userInput.split()

		if not cmdList:
			pass
		elif cmdList[0] == "cd":

			executeCD(cmdList[1])

		elif cmdList[0] == "ls":

			executeLS(cmdList)

		elif cmdList[0] == "pwd":

			executePWD()

		elif cmdList[0] == "touch":

			executeTouch(cmdList[1])

		elif cmdList[0] == "grep":

			executeGrep(cmdList[1],cmdList[2])

		elif cmdList[0] == "head":
			
			executeHead(cmdList)

		elif cmdList[0] == "tail":
			
			executeTail(cmdList)

		elif cmdList[0] == "tr":

			executeTR(cmdList)

		elif cmdList[0] == "sed":

			executeSed(cmdList)

		elif cmdList[0] == "diff":

			executeDiff(cmdList)

		elif cmdList[0] == "exit":

			sys.exit()

		elif cmdList[0]	== "clear":

			sys.stderr.write("\x1b[2J\x1b[H")

		else :
			print("> Command not found")										

if __name__ == "__main__":

	main()