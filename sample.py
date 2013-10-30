from saw import Saw
from saw.item import Item

text = "The next JavaScript specification is moving towards completion. \
TC39, the technical committee charged with creating ES.next (also known \
as ES Harmony, and sometimes ES 6) has already tentatively approved \
a number of proposals and there are a bunch more straw men awaiting approval. \
TC39 includes some of the finest minds in JavaScript (not least, Brendan Eich himself) \
but as Jeremy Ashkenas famously cautioned \"JavaScript is too important to be left \
to the experts\". They need our help."

#text = 'First sentence. Two, serios text?'

saw = Saw.load(text)
"""
for p in saw.paragraphs:
	for s in p.sentences:
		for b in s.blocks:
			for w in b.words:
				print '-----'

for a in saw.words:
	print '*-----'

for a in saw.sentences.words:
	print '&&----'

for a in saw.sentences[0].words:
	print '0----'
"""
#print saw

#print result


import datetime

with open('test.txt', 'r') as content_file:
    text = content_file.read()

st = datetime.datetime.now()

tr = text * 1
#Sentences.parse(tr)
saw = Saw.load(tr)
et = datetime.datetime.now()
print saw.sentences[2:6].blocks[2:].words
print '-------'
print saw.blocks[12]
print '-------'
print saw.blocks[12].words[:-2]
print '-------'
print saw.blocks[12].words[:-2:2]

if str(saw.blocks.words) == str(saw.words):
	print 'FUCK ME'


import sys

st = datetime.datetime.now()
a = []
_size = 0
for k in xrange(10000):
	i = Item()
	_size += sys.getsizeof(i)
	a.append(i)
et = datetime.datetime.now()

print "Memory: %s" % str(sys.getsizeof(a) + _size)
print "Time: %s" % str(et - st)
#print repr(saw)