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

# print pagecount

def htmlparser(testURL):
    r = s.get(testURL)
    rjson = r.json()
    flag=""
    for x in rjson['results']:
        if type(x['HELD_DATE'])== list:
            # print x['HELD_DATE'][1]
            helddate=x['HELD_DATE'][1]
        else:
            helddate=x['HELD_DATE']

        tag = x['TAG']
        url = x['URL']
        title = x['TITLE_INFO'][0]['title']

        hd = datetime(int(helddate.split('-')[0]),int(helddate.split('-')[1]),int(helddate.split('-')[2]))
        # print hd
        h_date = '{dt:%B} {dt.day}, {dt.year}'.format(dt=hd)

        print "TITLE : ",title," DATE : ",h_date.upper()," URL : ",url
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
        line_count=len(requiredDataList)
        if line_count < 10 and flag != tag:
            flag=tag
            print json.dumps({'TAG':tag,'LINE_COUNT': line_count,'TYPE': 'PDF','STATUS':'FAIL'})
        else:
            if flag != tag:
                flag = tag
                print json.dumps({'TAG':tag,'LINE_COUNT': line_count,'TYPE': 'TEXT','STATUS':'SUCCESS'})

            for x in requiredDataList:
                print json.dumps({'TAG': tag,'DATA': x, 'TITLE': title,'HELD_DATE':helddate})

for i in range(1,pagecount+1):
    htmlparser("https://dev.libraries.ou.edu/api-dsl/data_store/data/congressional/hearings/.json?page={0}".format(i))