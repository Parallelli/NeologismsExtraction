# -*- coding: utf-8 -*-
import codecs
import sys
from collections import defaultdict
reload(sys)
sys.setdefaultencoding('utf-8')

rawWords = file("allWords_file.txt")
dictWords = file("SogouDic.dic")
newWords = open("weiboInternetWords.txt","w")

sougouWords = {}
for line in dictWords:
	line =unicode(line,'utf-8')
	tokens = line.split()
	word = tokens[0]
	# word = unicode(tokens[0],'utf-8')
	# print line, len(word)
	if word not in sougouWords:
		sougouWords[word] = 1
dictWords.close()
	
internetwordsFreq = defaultdict(int)
for line in rawWords:
	utf8line = unicode(line,'utf-8')
	tokens = utf8line.split()
	word = tokens[0]
	if word not in sougouWords:
		print line	
		newWords.write(line)
newWords.close()
