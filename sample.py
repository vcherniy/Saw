from saw.saw import Saw
import datetime
import sys
from saw.node import Node

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
print '------- pure ---'
print saw.paragraphs[0]
print saw.paragraphs[0].pure()
print saw.paragraphs[0]

print ' ---- each ---'
kt = saw.sentences.each().words[:3].get()
for s in kt:
    print '** ' + str(s)
print ' ------- '


#IF blocks() then ERROR!!!!
# No works
#ps = saw.sentences.each().blocks.each().words[:3].get(2)

print '---------'

for s in saw.sentences[2:7]:
    print s[0][:10]

print '---------'
# should work
if saw.sentences[2:5].lower() == saw.sentences[2:5].each().lower().get(True):
	print 'saw.sentences.lower() == ssaw.sentences.each().lower().get(True)'

# get first block each paragraphs, save to variable, and lower it and save to another variable
result2 = saw.paragraphs.each().blocks[0].pure().lower().get()

for x in result2:
	print x.words, '-------'

txt = 'Fuck you, Bitch. Maza facka!'
sw = Saw.sentences.load(txt)
print sw.words.copy(lambda x: x.text(x._text + '_'))