from saw import Saw

text = "Starting right this second, it's way easier to merge Pull Requests! We usually merge them from the comfortable glow of our computers, but with the new mobile site we're comfortable merging smaller Pull Requests while sitting on the hyperloop (or while on the bus, I guess)."
"""
parse = Saw().load(text)
for bl in parse.paragraphs[0].sentences[0].blocks:
    print bl.words[:2]

print "---------- \n"
for bl in parse.blocks:
    print bl.words[:2]
"""

text = "The next JavaScript specification is moving towards completion. \
TC39, the technical committee charged with creating ES.next (also known \
as ES Harmony, and sometimes ES 6) has already tentatively approved \
a number of proposals and there are a bunch more straw men awaiting approval. \
TC39 includes some of the finest minds in JavaScript (not least, Brendan Eich himself) \
but as Jeremy Ashkenas famously cautioned \"JavaScript is too important to be left \
to the experts\". They need our help."

from saw.parser.sentences import Sentences
from saw.parser.blocks import Blocks
st = Sentences.parse(text)
result = []
for stnc in st:
	if isinstance(stnc, list):
		result.append(stnc)
	else:
		result.append(Blocks.parse(stnc))

print result