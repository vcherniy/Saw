from saw import Saw

text = "The next JavaScript specification is moving towards completion. \
TC39, the technical committee charged with creating ES.next (also known \
as ES Harmony, and sometimes ES 6) has already tentatively approved \
a number of proposals and there are a bunch more straw men awaiting approval. \
TC39 includes some of the finest minds in JavaScript (not least, Brendan Eich himself) \
but as Jeremy Ashkenas famously cautioned \"JavaScript is too important to be left \
to the experts\". They need our help."

text = 'First sentence. Two, serios text?'

saw = Saw().load(text)
for p in saw.paragraphs:
	for s in p.sentences:
		for b in s.blocks:
			for w in b.words:
				print '-----'

for a in saw.words:
	print '*-----'

#print result

"""
import datetime

with open('test.txt', 'r') as content_file:
    text = content_file.read()

st = datetime.datetime.now()

tr = text * 1
#Sentences.parse(tr)
saw = Saw().load(tr)
et = datetime.datetime.now()
print saw

print str(et - st)

t1 = ''
for p in saw:
	for s in p:
		if isinstance(s, list):
			for b in s:
				if isinstance(b, list):
					t1 = t1 + ' '.join(b)
				else:
					t1 = t1 + b + ' '
		else:
			t1 = t1 + s

print t1

"""