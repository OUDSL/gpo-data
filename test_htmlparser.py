import re
from urllib import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from nltk import sent_tokenize


#This is the date format you get from metadata
d = "2010-06-04"
x =  d.split('-')
year = x[0]
month=""
day=""
if x[1][0] == "0":
    month= x[1][1]
if x[2][0] == "0":
    day = x[2][1]

#This is the output you have to search in .htm files to get the start point to get our required data
z = datetime(2016,1,1).strftime("%A, %B %d, %Y")
print z

testURL = "https://www.gpo.gov/fdsys/pkg/CHRG-114hhrg93964/html/CHRG-114hhrg93964.htm"
soup = BeautifulSoup(urlopen(testURL),'html.parser')
startPOINT =  soup.getText().find("WEDNESDAY, MARCH 18, 2015")
requiredData = soup.getText()[startPOINT:].replace('\n'," ")
testData=re.sub(' +',' ',requiredData)
print testData
testData = sent_tokenize(testData)
for x in testData:
    print x
