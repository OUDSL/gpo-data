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

namesList=[]
congmemberList=[]
origininfoList=[]
languageList=[]
extensionList=[]
titleinfoList=[]
url=""
identifier=""
congcommitteeList=[]
witnessList=[]
helddate=""

# print json.dumps({'HELD_DATE':helddate,'URL':url,'NAMES':namesList,'CONG_MEMBERS':congmemberList,'ORIGIN_INFO':origininfoList,'EXTENSIONS':extensionList,'TITLE_INFO':titleinfoList,'IDENTIFIER':identifier,'CONG_COMMITTEE':congcommitteeList,'WITNESS':witnessList})

for x in soup('name'):
    if "namepart" in json.dumps(parse(str(x))):
        # print json.dumps(parse(str(x))['name']).replace("@",'').replace("#",'')
        namesList.append(json.dumps(parse(str(x))['name']).replace("@",'').replace("#",''))

for x in soup('congmember'):
    # print json.dumps(parse(str(x))['congmember']).replace("@",'').replace("#",'')
    congmemberList.append(json.dumps(parse(str(x))['congmember']).replace("@",'').replace("#",''))

for x in soup('origininfo'):
    # print json.dumps(parse(str(x))['origininfo']).replace("@",'').replace("#",'')
    origininfoList.append(json.dumps(parse(str(x))['origininfo']).replace("@",'').replace("#",''))

for x in soup('language'):
    # print json.dumps(parse(str(x))['language']).replace("@",'').replace("#",'')
    languageList.append(json.dumps(parse(str(x))['language']).replace("@",'').replace("#",''))

for x in soup('extension'):
    # print json.dumps(parse(str(x))['extension']).replace("@",'').replace("#",'')
    extensionList.append(json.dumps(parse(str(x))['extension']).replace("@",'').replace("#",''))

for x in soup('titleinfo'):
    if "@type" not in json.dumps(parse(str(x))):
        # print json.dumps(parse(str(x))['titleinfo']).replace("@",'').replace("#",'')
        titleinfoList.append(json.dumps(parse(str(x))['titleinfo']).replace("@",'').replace("#",''))

for x in soup('url'):
    if x['displaylabel'] == "HTML rendition":
        # print "{\"url\":\""+x.getText()+"\"}"
        url = "{\"url\":\""+x.getText()+"\"}"

for x in soup('identifier'):
    if "uri" in json.dumps(parse(str(x))):
        # print json.dumps(parse(str(x))['identifier']).replace("@",'').replace("#",'')
        identifier=json.dumps(parse(str(x))['identifier']).replace("@",'').replace("#",'')

for x in soup('congcommittee'):
    # print json.dumps(parse(str(x))['congcommittee']).replace("@",'').replace("#",'')
    congcommitteeList.append(json.dumps(parse(str(x))['congcommittee']).replace("@",'').replace("#",''))

for x in soup('witness'):
    # print json.dumps(parse(str(x))['witness']).replace("@",'').replace("#",'')
    witnessList.append(json.dumps(parse(str(x))['witness']).replace("@",'').replace("#",''))

for x in soup('extension'):
    if x.helddate:
        # print json.dumps(parse(str(x.helddate))['helddate'])
        helddate=json.dumps(parse(str(x.helddate))['helddate'])





# print json.dumps(parse(str(soup)))

load = json.dumps({'HELD_DATE':helddate,'URL':url,'NAMES':namesList,'CONG_MEMBERS':congmemberList,'ORIGIN_INFO':origininfoList,'EXTENSIONS':extensionList,'TITLE_INFO':titleinfoList,'IDENTIFIER':identifier,'CONG_COMMITTEE':congcommitteeList,'WITNESS':witnessList}).replace('\\','')

print load