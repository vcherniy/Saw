from saw.saw import Saw
import datetime
from saw.parsers.blocks import Blocks
import sys

with open('test.txt', 'r') as content_file:
    text = content_file.read()

start_time = datetime.datetime.now()

saw = Saw.load(text)

end_time = datetime.datetime.now()

print 'Time of text load - ' + str(end_time - start_time)

print saw.sentences[1:3].blocks[1:]
print '-------'
print saw.sentences[-3:].blocks[1:]
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
"""
kt = saw.sentences.each().words[:3].get()
for s in kt:
    print '** ' + str(s)
print ' ------- '

# IF blocks() then ERROR!!!!
# No works
#ps = saw.sentences.each().blocks.each().words[:3].get(2)

# RECURSION ERROR
#print ps2.inspect()


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
#print saw.sentences.lower() == saw.sentences.each().error.lower().get() == saw.sentences.each().lower().get()

# get first block each paragraphs, save to variable, and lower it and save to another variable
result = None
#result2 = saw.paragraphs.each().blocks[0].save_to(result).lower().get()
"""