# -*- coding: utf-8 -*-
import sys, codecs
from collections import defaultdict
import operator
import math
from zhon import hanzi
reload(sys)
sys.setdefaultencoding('utf-8')

# count total num of words(characters)
wordFreq = defaultdict(int)
word_tfidf = defaultdict(float)
wordDoc = defaultdict(int)
wordRightContext = defaultdict(list)
wordLeftContext = defaultdict(list)

weiboInternetWords = defaultdict(int)

#compute the freq of each fragment, and its left/right neighborhoods
def getFreq(infilename):
	InternetWords = defaultdict(int)
	for line in file("realInternetWords.txt"):
		line = unicode(line,'utf-8')
		word = line.split()[1]
		print word
		InternetWords[word] = 1
	InterCnt = 0

	readin = file(infilename)
	wordCnt = 0
	docCnt = 0
	wordFreqFile = open("wordFreq.txt","w")
	for line in readin:
		line = unicode(line,'utf-8')
		llen = len(line.strip())
		if llen < 1:
			continue
		docCnt += 1
		wordCnt += llen
		for i in range(0, llen):
			substr = ""
			if line[i] == ' ':
				continue
			for j in range(0,5): #i, i+1,...,i+4
				if i+j < llen:
					if line[i+j]==' ':
						break
					substr += line[i+j]
					if substr.strip() in InternetWords:
						InterCnt += 1
					if len(substr.strip())>=1:
						wordFreq[substr.strip()] += 1
					if i+j+1 < llen and line[i+j+1] != ' ':
						wordRightContext[substr.strip()].append(line[i+j+1])
					if i-1 >= 0 and line[i-1] != ' ':
						wordLeftContext[substr.strip()].append(line[i-1])
					preStr = line[:(i+j)]
					if substr.strip() not in preStr:
						wordDoc[substr.strip()] += 1
				else:
					break

	print "Internet words cnt: ", InterCnt
	# write the topk(k=5000) frequent fragments to file
	sorted_wordFreq = sorted(wordFreq.iteritems(),key=operator.itemgetter(1))
	sorted_word_tfidf = sorted(word_tfidf.iteritems(), key=(operator.itemgetter(1)))
	sorted_word_tfidf.reverse()
	sorted_wordFreq.reverse()
	# get topk wordFreq
	topk = 0
	topkWordFreq = open("topKFreqword.txt","w")
	for entry in sorted_wordFreq:
		cur_entry0 = entry[0]
		entry0len = len(cur_entry0)
		if entry0len >= 2:
			topk += 1
			if topk >= 5000:
				break
			topkWordFreq.write(entry[0].encode('utf-8')+'\t'+str(entry[1])+'\t'+str(wordDoc[entry[0]])+'\n')
	topkWordFreq.close()

	# get topk wordFreq_tfidf
	# write the topk(k=5000) tf-idf fragments to file
	topk = 0
	topkWordFreq_tfidf = open("topKFreqword_tfidf.txt","w")
	for entry in sorted_word_tfidf:
		cur_entry0 = entry[0]
		entry0len = len(cur_entry0)
		if entry0len >= 2:
			topk += 1
			if topk >= 5000:
				break
			topkWordFreq_tfidf.write(entry[0].encode('utf-8')+'\t'+str(entry[1])+'\t'+str(wordDoc[entry[0]])+'\n')
	topkWordFreq_tfidf.close()

	getMI()
	getLREntropy()
	getWordsList()

#For all snippts in wordFreq, compute their Mutual Information
# wordMI = np.array
wordMI = defaultdict(float)
wordDict = {}

def getMI():
	countWord = 0
	for k, v in wordFreq.items():
		# word = unicode(k,'utf-8')
		word = k
		vFreq = int(v)

		wlen = len(word)
		minMI = 1.0
		# print word, wlen, v
		for i in range(1, wlen): #enumerate all the substrings in word
			firstw = word[:i]
			secondw = word[i:]
			freq1 = wordFreq[firstw]
			freq2 = wordFreq[secondw]
			if freq1 == 0 or freq2 == 0:
				curMI = 0.0
			else:
				curMI = vFreq * math.log((1.0*vFreq)/(1.0*freq1*freq2))
			minMI = min(minMI, curMI)
		wordMI[word] = minMI
	sorted_wrodMI = sorted(wordMI.iteritems(), key=operator.itemgetter(1))
	
	#write the topk(k=5000) Mutual Information frequent fragments to file
	topkWord = open("topKMIword.txt","w")
	topk = 0
	for entry in sorted_wrodMI:
		# word = unicode(entry[0].encode('utf-8'),'utf-8')
		word = entry[0]
		if len(word)>=2: # test only output len>2 words
			# print word, len(word), entry[1]
			topkWord.write(word.encode('utf-8')+'\t'+str(entry[1])+'\t'+str(v)+'\n')
			topk+=1
			if topk >= 5000:
				break
	topkWord.close()


#For all snippts in wordFreq, compute their Mutual Information,
#Needs scan the input data **twice**, to get left(right) context
#Compute from 2 dict: wordLeftContext[], wordRightContext[]

wordLeftEntropy = defaultdict(float)
wordRightEntropy = defaultdict(float)

# compute left/right entropy of a fragment
def getLREntropy():
	# compute left entropy
	for k,v in wordLeftContext.items():
		leftwords = v
		lWordCnt = defaultdict(int)
		cur_entropy = 0.0
		lwordsCnt = len(v)
		for word in leftwords:
			lWordCnt[word]+=1
		for ik, iv in lWordCnt.items():
			cur_entropy += (-1.0*iv)/lwordsCnt*math.log((1.0*iv)/lwordsCnt)
		wordLeftEntropy[k] = cur_entropy

	# compute right entropy
	for k,v in wordRightContext.items():
		rightwords = v
		rWordCnt = defaultdict(int)
		cur_entropy = 0.0
		rwordsCnt = len(v)
		for word in rightwords:
			rWordCnt[word]+=1
		for ik, iv in rWordCnt.items():
			cur_entropy += (-1.0*iv)/rwordsCnt*math.log((1.0*iv)/rwordsCnt)
		wordRightEntropy[k] = cur_entropy

	sorted_leftWords = sorted(wordLeftEntropy.iteritems(), key=operator.itemgetter(1))
	testk = 0
	sorted_leftWords.reverse()
	sorted_rightWords = sorted(wordRightEntropy.iteritems(), key=operator.itemgetter(1))
	sorted_rightWords.reverse()


#ranking words with a score S(MI, LREntropy, Freq)
allWords = open("allWords_file.txt","w")
def getWordsList():
	for k, v in wordFreq.items():
		if len(k) < 2:
			continue
		word = k
		freq =int(v)
		miVal = wordMI[word]
		lrEntropy = min(wordLeftEntropy[word],wordRightEntropy[word])
		tfidf = word_tfidf[word]
		# freq, MI, LREntropy
		if freq > 12 and miVal <= -13.0 and lrEntropy >= 2.1 and tfidf >=10.0:
			word = word.encode('utf-8')
			allWords.write(word+'\t'+str(freq)+'\t'+str(miVal)+ '\t' + str(lrEntropy) +'\t'+str(tfidf)+'\n')

#compare with wordsDict, find the new one

if __name__ == '__main__':
	infilename = "data_clean_20k.txt" #default input file
	if len(sys.argv) > 1:
		infilename = sys.argv[1]
	getFreq(infilename)

