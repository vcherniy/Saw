from saw import Saw

text = "Starting right this second, it's way easier to merge Pull Requests! We usually merge them from the comfortable glow of our computers, but with the new mobile site we're comfortable merging smaller Pull Requests while sitting on the hyperloop (or while on the bus, I guess)."
parse = Saw().load(text)
for bl in parse.paragraphs[0].sentences[0].blocks:
    print bl.words[:2]

print "---------- \n"
for bl in parse.blocks:
    print bl.words[:2]
