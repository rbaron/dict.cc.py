#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import re
import sys

# Edit here for default number of results
MAX_RESULTS = 20

class Dict:
	def __init__(self):

		self.inputLanguage = "de"
		self.outputLanguage = "en"

		self.input = []
		self.output = []


	def setInputLanguage(self, lang):
		self.inputLanguage = lang

	def setOutputLanguage(self, lang):
		self.outputLanguage = lang

	def getResponse(self, word):
		# Trick to avoid dict.cc from denying the request: change User-agent to firefox's

		lang = self.inputLanguage + self.outputLanguage

		req = urllib2.Request("http://"+lang+".dict.cc/?s="+word, None,
                    {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
                )
		f = urllib2.urlopen(req)
		self.Response = f.read()


	# Find 'var c1Arr' and 'var c2Arr'
	def parseResponse(self):

		self.inputWords = []
		self.outputWords = []

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
			self.inputWords = re.findall(pattern, engLine)
			self.outputWords = re.findall(pattern, deLine)

	def printResults(self):
		if not self.inputWords or not self.outputWords:
			print "No results."

		else:
			# Get minumum number of both eng and de
			minWords = len(self.inputWords) if len(self.inputWords) <= len(self.outputWords) else len(self.outputWords)

			# Is it more than MAX_RESULTS?
			minWords = minWords if minWords <= MAX_RESULTS else MAX_RESULTS

			# Find biggest word in first col
			length = 0
			for w in self.inputWords[:minWords]:
				length = length if length > len(w) else len(w)

			for i in range(0,minWords):
				if self.inputWords[i] == "\"\"": continue
				#print self.inputWords[i].strip("\"") + "," + self.outputWords[i].strip("\"")
				print self.inputWords[i].strip("\"") + "."*(length - len(self.inputWords[i].strip("\"")) + 15) + self.outputWords[i].strip("\"")


if __name__ == "__main__":

	print "dict.cc.py:\n"

	if len(sys.argv) < 4:
		print "USAGE:\n$ dict.cc.py \"input language (e.g. DE for German)\" \"output language e.g. EN for English)\" \"word\" (without the \"s)"
	else:
		# Concat all arguments into one word (urlencoded space)
		expression = ""

		inputFromSysArgv = sys.argv[1].upper()
		outputFromSysArgv = sys.argv[2].upper()

		for index in range(3, len(sys.argv)):
			expression += sys.argv[index] + " "

		print inputFromSysArgv + " to " + outputFromSysArgv + ": " + expression + "\n"

		# Urlencode input
		expression = urllib.quote(expression)

		myDict = Dict()
		myDict.setInputLanguage( inputFromSysArgv )
		myDict.setOutputLanguage( outputFromSysArgv )
		myDict.getResponse(expression)
		myDict.parseResponse()
		myDict.printResults()
