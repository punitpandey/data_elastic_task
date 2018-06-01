from __future__ import unicode_literals
import math
import requests
import urllib
import json
from bs4 import BeautifulSoup
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
BASE_URL="https://health.usnews.com"

def getCities(country_short_code):
    """function to return cities"""
    Ulist=[]
    URL=BASE_URL+"/doctors/city-index/new-jersey"
    data=requests.get(URL,headers=headers)
    soup=BeautifulSoup(data.content,'html.parser')
    for list in soup.find_all("li",class_="index-item"):
        hlink=list.a
        # print hlink.text.strip()
        Ulist.append(hlink.get("href"))
    # print(Ulist)
    getSpecs(hlink.get("href"),country_short_code,hlink.text.strip())

def getSpecs(specsURL,country_short_code,city):
    """function to return specialities"""
    Ulist=[]
    URL=BASE_URL+specsURL
    data=requests.get(URL,headers=headers)
    soup=BeautifulSoup(data.content,'html.parser')
    for list in soup.find_all("li",class_="index-item"):
        hlink=list.a
        # print hlink.text.strip()
        Ulist.append(hlink.get("href"))
    # print(Ulist)
    getDocs(hlink.get("href"),country_short_code,city,hlink.text.strip())

def getDocs(docsURL,country_short_code,city,specialty):
    """to return doctors for specific specialities"""
    Ulist=[]
    URL=BASE_URL+'/health-care/doctors/search-data?distance=20&location='+city.title()+', '+country_short_code+'&specialty='+specialty
    data=requests.get(URL,headers=headers)
    soup=BeautifulSoup(data.content,'html.parser')
    newDictionary=json.loads(str(soup))
    doctors_count=newDictionary["results"]["doctors"]["totalMatches"]
    page=2
    while page <= math.ceil(doctors_count/20.0):
        print page
        page+=1

getCities('NJ')
