import re
from datetime import date
from bs4 import BeautifulSoup
import pymysql
from urllib.request import Request, urlopen
from nltk.corpus import stopwords
import requests
stopWords = set(stopwords.words('english'))

date1 = str(input("Enter your date in yyyy/mm/dd:"))
reason1= str(input("Enter your query:"))

year1,month1,day1 =map(int, date1.split('/'))

a= date(2001,1,1)
b=date(year1,month1,day1)
var=b-a
result=var.days + 36892
link="https://timesofindia.indiatimes.com/"+str(date1)+"/archivelist/year-"+str(year1)+",month-"+str(month1)+",starttime-"+str(result)+".cms"

req= requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})

bsObj= BeautifulSoup(req.text,'lxml')

reason1=reason1.lower()
tags=bsObj.find_all('a')
lst=[]
for tag in tags:
    var1=tag.get('href')
    var2=tag.text
    var2=var2.lower()
    x=re.findall(reason1,var2)
    if(len(x)!=0):
        if("http://timesofindia.indiatimes.com/" or "https://timesofindia.indiatimes.com/" not in var1):
            var1="http://timesofindia.indiatimes.com/"+str(var1)
            lst.append(var1)
        else:
            lst.append(var1)
article=[]
if(len(lst)==0):
    print("No news found")
else:
    for i in lst:
        html1= requests.get(i,headers={'User-Agent': 'Mozilla/5.0'})
        bsobj1= BeautifulSoup(html1.text,'lxml')
        var4= bsobj1.findAll("div",{"class":"Normal"})
        str1=""
        try:
            for j in var4:
                str1=str1+str(j.text)
                
        except:
            pass
        article.append(str1)
article = list(filter(None, article))

for i in range(len(article)):
    article[i] = article[i].split()

d={}
for i in article:
    for x in i:
        if(x not in d.keys() and x not in stopWords):
            d[x]=0
d1={}
for i in article:
    for x in i:
        if(x not in d1.keys() and x not in stopWords):
            d1[x]=0

for i in range(len(article)): 
    for word in article[i]:
        if(word not in stopWords):
            d[word] +=1

l=''
m=0
for k in d.keys():
    if (d[k]>m):
        m=d[k]
        l=k
count=len(d.keys())
for i in d.keys():
    d[i] =d[i]/count


pol=[]
var
for i in d.keys():
    pol.append(i)


new=[]
new1=[]
for i in range(len(pol)):
    count=0
    for j in range(len(article)):
        for k in range(len(article[j])):
            if(pol[i] in article[j][k]):
                count+=1
    new.append(count)
    new1.append(count)
res = {} 
for key in pol: 
    for value in new: 
        res[key] = value 
        new.remove(value) 
        break

idf=[]
import math

for i in range(len(pol)):
    u=math.log(len(article)/new1[i])
    idf.append(u)

idfs={}
for key in pol: 
    for value in idf: 
        idfs[key] = value 
        idf.remove(value) 
        break

print("TF values are: " )
print(d)
print("\nIDF values are: ")
print(idfs)
