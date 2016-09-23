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
flag=""
print pagecount

def htmlparser(testURL):
    r = s.get(testURL)
    rjson = r.json()
    titleList=[]
    dateList =[]
    htmlList = []
    tagLIST=[]
    for x in rjson['results']:
        if type(x['HELD_DATE'])== list:
            # print x['HELD_DATE'][1]
            dateList.append(x['HELD_DATE'][1])
        else:
            # print x['HELD_DATE']
            dateList.append(x['HELD_DATE'])


    for x in rjson['results']:
        # print x['URL']
        htmlList.append(x['URL'])

    for x in rjson['results']:
        for y in x['EXTENSIONS']:
            if "searchtitle" in y:
                # print y['searchtitle']
                titleList.append(y['searchtitle'])

    for x in rjson['results']:
        # print x['TAG']
        tagLIST.append(x['TAG'])

    for i,url in enumerate(htmlList):
        hd = datetime(int(dateList[i].split('-')[0]),int(dateList[i].split('-')[1]),int(dateList[i].split('-')[2]))
        h_date = '{dt:%B} {dt.day}, {dt.year}'.format(dt=hd)
        # print "TITLE : ",titleList[i]," DATE : ",h_date.upper()," URL : ",url
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
        global flag
        if line_count < 10 and flag != tagLIST[i]:
            flag=tagLIST[i]
            print json.dumps({'TAG':tagLIST[i],'LINE_COUNT': line_count,'TYPE': 'PDF','STATUS':'FAIL'})
        else:
            if flag != tagLIST[i]:
                flag = tagLIST[i]
                print json.dumps({'TAG':tagLIST[i],'LINE_COUNT': line_count,'TYPE': 'TEXT','STATUS':'SUCCESS'})

            for x in requiredDataList:
                print json.dumps({'TAG': tagLIST[i],'DATA': x, 'TITLE': titleList[i],'HELD_DATE':dateList[i]})




for i in range(1,pagecount+1):
    htmlparser("https://dev.libraries.ou.edu/api-dsl/data_store/data/congressional/hearings/.json?page={0}".format(i))

# htmlparser(testURL)





