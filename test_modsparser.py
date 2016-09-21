import json
import re

from urllib import urlopen

from xmltodict import parse
from bs4 import BeautifulSoup
from datetime import date, datetime, time
from nltk import sent_tokenize

xmlURL = "https://www.gpo.gov/fdsys/pkg/CHRG-112hhrg66204/mods.xml"
r = urlopen(xmlURL)
soup = BeautifulSoup(r,'html5lib')


for x in soup('name'):
    if "namepart" in json.dumps(parse(str(x))):
        print json.dumps(parse(str(x)))

for x in soup('congmember'):
    print json.dumps(parse(str(x)))

for x in soup('origininfo'):
    print json.dumps(parse(str(x)))

for x in soup('language'):
    print json.dumps(parse(str(x)))

for x in soup('origininfo'):
    print json.dumps(parse(str(x)))

for x in soup('extension'):
    print json.dumps(parse(str(x)))

for x in soup('titleinfo'):
    if "@type" not in json.dumps(parse(str(x))):
        print json.dumps(parse(str(x)))

for x in soup('url'):
    if x['displaylabel'] == "HTML rendition":
        print "{\"url\":\""+x.getText()+"\"}"

for x in soup('identifier'):
    if "uri" in json.dumps(parse(str(x))):
        print json.dumps(parse(str(x)))

for x in soup('congcommittee'):
    print json.dumps(parse(str(x)))

for x in soup('witness'):
    print json.dumps(parse(str(x)))

# if "namepart" in json.dumps(parse(str(soup('name')[0]))):
#     print "HI"

