#! /usr/bin/env python

import re
import sys
import itertools

# create the dictionary of ARPAbet definitions and groups

arpa_dict = {
'AO': 'Monophthong',
'AA': 'Monophthong',
'IY': 'Monophthong',
'UW': 'Monophthong',
'EH': 'Monophthong',
'IH': 'Monophthong',
'UH': 'Monophthong',
'AH': 'Monophthong',
'AX': 'Monophthong',
'AE': 'Monophthong',
'EY': 'Diphthong',
'AY': 'Diphthong',
'OW': 'Diphthong',
'AW': 'Diphthong',
'OY': 'Diphthong',
'ER': 'R-colored vowel',
'AXR': 'R-colored vowel',
'P': 'Stop',
'B': 'Stop',
'T': 'Stop',
'D': 'Stop',
'K': 'Stop',
'G': 'Stop',
'CH': 'Affricate',
'JH': 'Affricate',
'F': 'Fricative',
'V': 'Fricative',
'TH': 'Fricative',
'DH': 'Fricative',
'S': 'Fricative',
'Z': 'Fricative',
'SH': 'Fricative',
'ZH': 'Fricative',
'HH': 'Fricative',
'M': 'Nasal',
'EM': 'Nasal',
'N': 'Nasal',
'EN': 'Nasal',
'NG': 'Nasal',
'ENG': 'Nasal',
'L': 'Liquid',
'EL': 'Liquid',
'R': 'Liquid',
'DX': 'Liquid',
'NX': 'Liquid',
'Y': 'Semivowel',
'W': 'Semivowel',
'Q': 'Semivowel'
}

list_monophthong = ['AO','AA','IY','UW','EH','IH','UH','AH','AX','AE']
list_diphthong = ['EY','AY','OW','AW','OY']
list_rvowel = ['ER','AXR']
list_stop = ['P','B','T','D','K','G']
list_affricate = ['CH','JH']
list_fricative = ['F','V','TH','DH','S','Z','SH','ZH','HH']
list_nasal = ['M','EM','N','EN','NG','ENG']
list_liquid = ['L','EL','R','DX','NX']
list_semivowel = ['Y','W','Q']

# create the dictionary of ARPAbet pronunciations

flatfile = open( "cmudict.0.7a.txt", "r" )

pronounce_dict = {}

for line in flatfile:
	line = line.rstrip("\n")
	if (re.match( r"^\w", line, re.I) != None ):
		print( line )
		key, val = line.split("  ")
		pronounce_dict[ key ] = val

flatfile.close()

print "Value : %s" % pronounce_dict.values()

# read input and match dict entry, and print the ARPAbet notation

while True:
	word = raw_input("Enter a word: ")		# take the input
	word = word.rstrip("\n") 				# strip the newline
	word = word.upper() 					# convert it to uppercase
	
	try:
		phonemes = pronounce_dict[ word ]	# get the string of ARPAbet phonemes
		phonemes = phonemes.split(" ")
		print phonemes						# print the string of ARPAbet phonemes
	except KeyError:
		print "No matches found"			# if it's not found, continue
		continue

	# enter in a binary mask, indicating which ARPAbet phonemes to match on
	# on a touch interface, you would use your finger to manipulate the phonemes
	# match, don't match, or match group

	while True:
		mask = raw_input("Enter the rhyme mask: ")
		mask = mask.rstrip("\n")
		# error check: test that it's just 1s and 0s, test that it's the correct length
		if (re.match( r"^[01-]{%d}$" % len(phonemes), mask ) == None ):
			print "Error: check your mask format! It needs to be %d characters long, and only 1s and 0s!" % len(phonemes)
			continue
		else:
			break

	# get the rhymes from the dict, and print them back	
	
	# will need to keep a count of how many vowels exist in the word
	# are num vowels = num syllables? appears so!
	# sometimes you want to ignore the stress value at the end of a vowel

	# ignore stress value
	# count syllables
	
	# this function sucks because it is a very sloppy way to get a string into a list
	# matchy_chunk.append( phoneme_no_stress.split(" ") )
	# and because there must be a better way to get the list of ARPA types into a list
	# besides that huge elif statement
	count_vowels = 0
	pos = 0
	matchy_chunk = []
	for phoneme in phonemes:
		phoneme_no_stress = re.sub( r"\d$", "", phoneme )
		print phoneme_no_stress
		if mask[ pos ] == "1":
			matchy_chunk.append( phoneme_no_stress.split(" ") )
		elif mask[ pos ] == "-":
			if arpa_dict[ phoneme_no_stress ] == "Monophthong":
				matchy_chunk.append( list_monophthong )
			elif arpa_dict[ phoneme_no_stress ] == "Diphthong":
				matchy_chunk.append( list_diphthong )
			elif arpa_dict[ phoneme_no_stress ] == "R-colored vowel":
				matchy_chunk.append( list_rvowel )
			elif arpa_dict[ phoneme_no_stress ] == "Stop":
				matchy_chunk.append( list_stop )
			elif arpa_dict[ phoneme_no_stress ] == "Affricate":
				matchy_chunk.append( list_affricate )
			elif arpa_dict[ phoneme_no_stress ] == "Fricative":
				matchy_chunk.append( list_fricative )
			elif arpa_dict[ phoneme_no_stress ] == "Nasal":
				matchy_chunk.append( list_nasal )
			elif arpa_dict[ phoneme_no_stress ] == "Liquid":
				matchy_chunk.append( list_liquid )
			elif arpa_dict[ phoneme_no_stress ] == "Semivowel":
				matchy_chunk.append( list_semivowel )
		pos += 1
	print matchy_chunk
	
	from itertools import product
	thing = ["|".join(map(str,x)) for x in product(*matchy_chunk)]
	print thing
			
	

	for dictitem in pronounce_dict.items():
		pronunciation = dictitem[1].split(" ")
		pos = 0
		dicty_chunk = []
		for phoneme in pronunciation:
			dicty_chunk.append( re.sub( r"\d$", "", phoneme ) )
			pos += 1
#		stuff = '|'.join(matchy_chunk)
		stuff2 =  '|'.join(dicty_chunk)
		for stuff in thing:
			if stuff in stuff2:
				print dictitem[0]
			
# strip the stress value of the dictionary entry
# strip the stress value of the word
# reverse the dictionary entry
# reverse the word
# reverse the mask
# compare the dictionary entry, word, and mask
# iterate through the word and find the first vowel that the mask indicates must match
# look on either side of that until you get to a zero
# so for instance if its "change"
# 	CH	EY	N	JH
#	1	1	0	0
# it knows that it has to look for a chain of two phonemes 

# mask values:
# 1 means it must match
# - means it must match the same group
# 0 means it doesn't have to match
# ~ at the beginning or end means the match can be longer

# if the matching chunk starts at the beginning of the word, then match beginnings only
# if the matching chunk starts at the end of the word, then match ends only
# if the matching chunk is in the middle of the word, and doesn't touch an end, match anywhere

# don't allow two discrete matching chunks to be specified in a single word

# at the end, also match silent stops
# reflex, pretext, recess

# clean up, pythonify, refactor, rename variables
# convert to c
# attempt to build into ios app
# then add text editor to ios app
# then add icloud support to ios app
# then add airprint support to ios app

#rhyme