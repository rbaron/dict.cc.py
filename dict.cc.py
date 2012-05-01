#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import re
import sys

# Edit here for default number of results
MAX_RESULTS = 20

class Dict:
	def __init__(self):
		self.Eng = []
		self.De = []

	def getResponse(self, word):
		# Trick to avoid dict.cc from denying the request: change User-agent to firefox's
		req = urllib2.Request("http://www.dict.cc/?s="+word, None, {'User-agent': 'Mozilla/5.0'})
		f = urllib2.urlopen(req)
		self.Response = f.read()
	
	# Find 'var c1Arr' and 'var c2Arr' 
	def parseResponse(self):
		
		self.engWords = []
		self.deWords = []

		engLine = deLine = ""

		# Split lines
		lines = self.Response.split("\n")

		for l in lines:
			if l.find("var c1Arr") >= 0:
				engLine =  l
			elif l.find("var c2Arr") >= 0:
				deLine = l

		if not engLine or not deLine:
			return False

		else:
			# Regex
			# pattern = "\"[A-Za-z \.()\-\?ßäöüÄÖÜéáíçÇâêî\']*\""
			pattern = "\"[^,]+\""

			# Return list of matching strings
			self.engWords = re.findall(pattern, engLine)
			self.deWords = re.findall(pattern, deLine)

	def printResults(self):
		if not self.engWords or not self.deWords:
			print "No results."

		else:
			# Get minumum number of both eng and de
			minWords = len(self.engWords) if len(self.engWords) <= len(self.deWords) else len(self.deWords)

			# Is it more than MAX_RESULTS?
			minWords = minWords if minWords <= MAX_RESULTS else MAX_RESULTS

			# Find biggest word in first col
			length = 0
			for w in self.engWords[:minWords]:
				length = length if length > len(w) else len(w)

			
			# Nice output
			print "English" + " "*(length - len("English") + 15) + "Deutsch"
			print "=======" + " "*(length - len("English") + 15) + "=======\n"
			for i in range(0,minWords):
				if self.engWords[i] == "\"\"": continue
				print self.engWords[i].strip("\"") + "."*(length - len(self.engWords[i].strip("\"")) + 15) + self.deWords[i].strip("\"")


if __name__ == "__main__":

	print "dict.cc.py:\n"

	if len(sys.argv) < 2:
		print "USAGE:\n$ dict.cc.py \"word\" (without the \"s)"
	else:
		# Concat all arguments into one word (urlencoded space)
		expression = ""
		for index in range(1, len(sys.argv)):
			expression += sys.argv[index] + " "

		print "Interpreted input: " + expression + "\n"
		
		# Urlencode input
		expression = urllib.quote(expression)

		myDict = Dict()
		myDict.getResponse(expression)
		myDict.parseResponse()
		myDict.printResults()
