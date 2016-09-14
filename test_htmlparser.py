import json
import requests
from xmltodict import parse
from datetime import datetime


testURL="https://dev.libraries.ou.edu/api-dsl/data_store/data/congressional/hearings/?format=json"
s = requests.session()
r = s.get(testURL).text
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

for i,url in enumerate(htmlList):
    y = datetime.strptime(dateList[i],"%Y-%m-%d")
    sdate = y.strftime("%B %d, %Y")
    print sdate,url