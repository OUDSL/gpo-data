import json
import re
import requests
from nltk import sent_tokenize
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep


s = requests.session()
testURL="https://dev.libraries.ou.edu/api-dsl/data_store/data/congressional/hearings/?format=json"
r = s.get(testURL)
rjson = r.json()
pagecount = rjson['meta']['pages']
print pagecount

def htmlparser(testURL):
    r = s.get(testURL).text
    titleList=[]
    dateList =[]
    htmlList = []
    rjson =  json.loads(r)
    for x in rjson['results']:
        for y in x['mods']['extension']:
            if "heldDate" in y:
                if type(y['heldDate'])== list:
                    dateList.append(y['heldDate'][1])
                else:
                    dateList.append(y['heldDate'])


    for x in rjson['results']:
        for y in x['mods']['location']['url']:
            if y['displayLabel'] == "HTML rendition":
                htmlList.append(y['text'])

    for x in rjson['results']:
        for y in x['mods']['titleInfo']:
            if "title" in y:
                titleList.append(y['title'])

    for i,url in enumerate(htmlList):
        hd = datetime(int(dateList[i].split('-')[0]),int(dateList[i].split('-')[1]),int(dateList[i].split('-')[2]))
        h_date = '{dt:%B} {dt.day}, {dt.year}'.format(dt=hd)
        print "TITLE : ",titleList[i]," DATE : ",h_date.upper()," URL : ",url
        try:
            soup = BeautifulSoup(s.get(url).text,'html.parser')
        except:
            sleep(60)
            soup = BeautifulSoup(s.get(url).text,'html.parser')

        startPoint = soup.text.find(h_date.upper())
        requiredData = soup.text[startPoint::].replace('\n'," ")
        requiredData = re.sub(' +',' ',requiredData)
        requiredDataList = sent_tokenize(requiredData)
        print "NUMBER OF SENTENCES ---> ",len(requiredDataList),"\n"


for i in range(1,pagecount+1):
    htmlparser("https://dev.libraries.ou.edu/api-dsl/data_store/data/congressional/hearings/.json?page={0}".format(i))

# print rjson['results'][0]['mods']['titleInfo'][0]['title']

