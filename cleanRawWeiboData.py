# -*- coding: utf-8 -*-
import sys
import numpy as np
from zhon import hanzi
import codecs
import re
#usage:
#python cleanRawData.py inputfilepath(first argument)
#what will be done?
#Remove @XX (repost from), http://...(location or reference information)
englishPunc = [',','...','.',':','[',']','<','?','!','>','~','*','(',')','^','_','#','+','-']
stopWords = '啊呀哦哈'
stopWords = unicode(stopWords, 'utf-8')

def clear(inFile):
	raw = file(inFile)
	clearv = open('data_clean_20k.txt','w')
	wordCnt = 0
	outline = ''
	waitcolon = False
	for line in raw:
		line = unicode(line, 'utf-8')
		l = len(line)
		outline = ''
		waitcolon = False
		preChar=''
		for i in range(0,l):
			if re.match('^[0-9a-zA-Z]+$',line[i]):
				if preChar != ' ':
					outline += ' '
					preChar = ' '
			elif line[i] in stopWords:
				if preChar != ' ':
					outline += ' '
					preChar = ' '
			elif line[i] == '@':
				waitcolon = True
				preChar = '@'
			elif line[i] == ':':
				if waitcolon == True:
					waitcolon = False
				else:
					if preChar != ' ':
						outline+=' '
						preChar = ' '
			elif line[i] in hanzi.punctuation or line[i] in englishPunc:
				if preChar !=  ' ':
					outline += ' '
					preChar = ' '
			else:
				if waitcolon == False and line[i]<>'/':
					outline += line[i]
					preChar = line[i]
		newl = len(outline)
		if newl > 1 and outline[newl-1] <> '\n':
			outline += '\n'
		clearv.write(outline.encode('utf-8'))
	clearv.close()

if __name__ == "__main__":
	inFile = 'weibo_raw_userlistweibo_big.txt'
	if len(sys.argv) > 1:
		inFile = sys.argv[1] #first argu denotes data path
	clear(inFile)

