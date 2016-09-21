import json
from time import sleep

from requests import session
from xmltodict import parse
from bs4 import BeautifulSoup


def load_xml_json(xmlURL):
    s=session()
    try:
        s = s.get(xmlURL)
        soup = BeautifulSoup(s.text,'html5lib')
    except:
        sleep(60)
        s = s.get(xmlURL)
        soup = BeautifulSoup(s.text,'html5lib')

    namesList=[]
    congmemberList=[]
    origininfoList=[]
    languageList=[]
    extensionList=[]
    titleinfoList=[]
    url=""
    pdf=""
    identifier=""
    congcommitteeList=[]
    witnessList=[]
    helddate=""

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
            # url = "{\"url\":\""+x.getText()+"\"}"
            url=x.getText()
            # print url
        if x['displaylabel'] == "PDF rendition":
            # pdf = "{\"pdf\":\""+x.getText()+"\"}"
            pdf = x.getText()
            # print pdf

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

    tag = url.split('/')[5]

    data = json.dumps({'TAG':tag,'HELD_DATE':helddate,'URL':url,'PDF':pdf,'NAMES':namesList,'CONG_MEMBERS':congmemberList,'ORIGIN_INFO':origininfoList,'EXTENSIONS':extensionList,'TITLE_INFO':titleinfoList,'IDENTIFIER':identifier,'CONG_COMMITTEE':congcommitteeList,'WITNESS':witnessList}).replace('\\','')

    # print data

