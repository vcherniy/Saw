from saw import Saw
from saw.item import Item
import datetime
import sys

with open('test.txt', 'r') as content_file:
    text = content_file.read()

start_time = datetime.datetime.now()

saw = Saw.load(text)

end_time = datetime.datetime.now()
print 'Time of text load - ' + str(end_time - start_time)

print saw.sentences[2:6].blocks[2:].words
print '-------'
print saw.blocks[12]
print '-------'
print saw.blocks[12].words[:-2]
print '-------'
print saw.blocks[12].words[:-2:2]

if str(saw.blocks.words) == str(saw.words):
	print 'str(saw.blocks.words) == str(saw.words)'
print '-------'

print ' ---- each ---'
kt = saw.sentences.each().blocks.pure().words[:3].get()
for s in kt:
	print '** ' + str(s)
print ' ------- '

start_time = datetime.datetime.now()
a = []
_size = 0
for k in xrange(10000):
	i = Item()
	_size += sys.getsizeof(i)
	a.append(i)
end_time = datetime.datetime.now()

print "Memory: %s" % str(sys.getsizeof(a) + _size)
print "Time: %s" % str(end_time - start_time)
print '---------'

for s in saw.sentences[5:7]:
	print s[:3]

print '---------'


# should work
saw.sentences.lower().words == saw.sentences.each().this.lower().get().words == saw.sentences.each().lower().get().words

# get first block each paragraphs, save to variable, and lower it and save to another variable
result = None
result2 = saw.paragraphs.each().blocks[0].save_to(result).lower().get()


