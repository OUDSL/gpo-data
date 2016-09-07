import json
import re
from urllib import urlopen
from urlparse import urlparse, parse_qs
from bs4 import BeautifulSoup
from xmltodict import parse

#To get updated hearings links

mainURL="https://www.gpo.gov"
jsonFile = {}
filterLinks = []

def mainLinks():
    hearingsURL = "https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=114&isCollapsed=true&leafLevelBrowse=false&ycord=0"

    r = urlopen(hearingsURL)

    soup = BeautifulSoup(r,'html.parser')

    test = soup.findAll('input',{"name":"urlhid"})

    for i in test:
        print mainURL+i.get('value').replace("amp;","")
        # level1(mainURL+i.get('value').replace("amp;",""))
    level1("https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=112&isCollapsed=false&leafLevelBrowse=false")
#****************************************************************************************************************#
#Getting links for HOUSE || JOINT || SENATE
def level1(url):
#This is for getting links for HOUSE || JOINT || SENATE
    # test = "https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=113&isCollapsed=false&leafLevelBrowse=false"
    test = url
    r = urlopen(test)

    soup = BeautifulSoup(r,"html.parser")

    # print soup.prettify()

    test = soup.findAll('div',class_="browse-level")


    for i in test:
        if "FHOUSE" in i.a["onclick"]:
            # print mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',i.a["onclick"])[0]
            level2(mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',i.a["onclick"])[0])
        elif "FJOINT" in i.a["onclick"]:
            # print mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',i.a["onclick"])[0]
            level2(mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',i.a["onclick"])[0])
        elif "FSENATE" in i.a["onclick"]:
            # print mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',i.a["onclick"])[0]
            level2(mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',i.a["onclick"])[0])


    # test = "goWithVars('/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=114%2FHOUSE&isCollapsed=false&leafLevelBrowse=false',''); return false;"
    # test = "q2///ftp://www.somewhere.com/over/the/rainbow/image.jpg"
    # print re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)',test)[0]


#This gives House || Senate || Joint links for extending
def level2(url):
    # test = "https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=114%2FHOUSE&isCollapsed=false&leafLevelBrowse=false"
    test = url
    r = urlopen(test)

    soup = BeautifulSoup(r,"html.parser")

    filteredDiv = []
    for i in soup('div'):
        for j in i('div'):
            for k in j('div'):
                filteredDiv.append(k)

    l2 = []
    for i in filteredDiv:
        if i('div') and "browse-level" in i('div')[0]['class']:
            for j in i.findAll('div',class_="level2 browse-level"):
                l2.append(j)

    for i in l2:
        for j in i('a'):
            # print mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)', j['onclick'])[0].replace("isCollapsed=true","isCollapsed=false")
            level3(mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\'\'\);)', j['onclick'])[0].replace("isCollapsed=true","isCollapsed=false"))

    test=""


#Get the links to get options for HTML | PDF | MORE
def level3(url):
    # test ="https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=114%2FHOUSE&isCollapsed=false&leafLevelBrowse=false"
    test = url
    r = urlopen(test)

    soup = BeautifulSoup(r,"html.parser")

    for i in soup.findAll('div', class_="level3"):
        for j in i('a'):
            # print "Title --> "+j.getText().strip()+"  "+mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\')', j['onclick'])[0].replace("isCollapsed=true","isCollapsed=false")
            morePageLinks(mainURL+re.findall(r'(?<=goWithVars\(\').*?(?=\',\')', j['onclick'])[0].replace("isCollapsed=true","isCollapsed=false"))

#More page links
def morePageLinks(url):
    # test = "https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CHRG&browsePath=114%2FHOUSE%2FCommission+on+Security+and+Cooperation+in+Europe&isCollapsed=false&leafLevelBrowse=false&isDocumentResults=true"
    test = url
    r = urlopen(test)
    soup = BeautifulSoup(r,"html.parser")

    # print soup.prettify()
    for i in soup.findAll('a'):
        if i.get('href')!=None and "search/page" in i.get('href'):
            if mainURL+"/fdsys/"+i.get('href') not in filterLinks:
                filterLinks.append(mainURL+"/fdsys/"+i.get('href'))
                url =  mainURL+"/fdsys/"+i.get('href')
                parseURL = urlparse(url)
                id = parse_qs(parseURL.query)['packageId'][0]
                modsURL =  "https://www.gpo.gov/fdsys/pkg/"+id+"/mods.xml"
                modsParser(modsURL)

#Parses the mods.xml files
def modsParser(url):
    xmlURL = url
    r = urlopen(xmlURL)
    x = json.dumps(parse(r.read())).replace("@",'').replace("#",'')
    print json.dumps(json.loads(x),indent=4)

mainLinks()
