from __future__ import unicode_literals
import requests
import json
import csv
from datetime import datetime
from bs4 import BeautifulSoup
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
BASE_URL="https://health.usnews.com"
doctorsData=[]
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
    # to write all data at once
    writeData()

def getDocs(docsURL,country_short_code,city,specialty):
    """to return doctors for specific specialities"""
    Ulist=[]
    page=1
    hasNextPage=True
    while hasNextPage is True:
        URL=BASE_URL+'/health-care/doctors/search-data?distance=20&location='+city.title()+', '+country_short_code+'&specialty='+specialty+'&page='+str(page)
        data=requests.get(URL,headers=headers)
        soup=BeautifulSoup(data.content,'html.parser')
        newDictionary=json.loads(str(soup))
        hasNextPage=newDictionary["results"]["doctors"]["hasNextPage"]
        page+=1
        # doctors parsing
        for doc in newDictionary["results"]["doctors"]["matches"]:
            docURL=doc["url"].strip()
            Ulist.append(docURL)
            # print str(docURL)
            getDoc(docURL)
    # print len(Ulist)
    # print page
def getDoc(docURL):
    """function to get doctor information"""
    try:
        URL=BASE_URL+docURL
        data=requests.get(URL,headers=headers)
        soup=BeautifulSoup(data.content,'html.parser')
        overview=soup.find("section",attrs={'class': 'profile-overview'}).find('p').text.strip()
        # print overview
        raw_name=soup.find('h1',attrs={'class':'doctor-name'})
        remove_span=raw_name.find('span')
        remove_span.extract()
        name=raw_name.text.strip()
        # print name
        practiceYears=soup.find("section",attrs={'class': 'profile-overview'}).select('div:nth-of-type(2)')[0].select('div:nth-of-type(2)')[0].select('span:nth-of-type(3)')[0].text.strip()
        # print practiceYears
        language=soup.find("section",attrs={'class': 'profile-overview'}).select('div:nth-of-type(2)')[0].select('div:nth-of-type(5)')[0].select('span:nth-of-type(3)')[0].text.strip()
        # print language
        officeLocation=soup.find('span',attrs={'data-js-id':'doctor-address'}).text.strip()
        # print officeLocation
        hostelAffi=[]
        hospitalAffiliations=soup.find('section',attrs={'data-nav-waypoint':'hospitals'})
        for hospitalAffiliation in hospitalAffiliations.find_all('a',class_="heading-larger block-tight"):
            if hospitalAffiliation.get("href") and hospitalAffiliation.get("href")!="":
                hostelAffi.append(str(hospitalAffiliation.text.strip()))
                # print hostelAffi
        experience=soup.find("section",attrs={'data-nav-waypoint':'experience'}).div.div
        specS=[]
        for specs in experience.find_all('a',class_='text-large'):
            specS.append(str(specs.text.strip()))
            # print specS
        subSpecs=[]
        for subspec in experience.find_all('p',class_='text-large'):
            subSpecs.append(str(subspec.text.strip()))
            # print subSpecs
        eduS=[]
        educations=soup.find("section",attrs={'data-nav-waypoint':'experience'}).findNext("section")
        for edu in educations.find_all("li"):
            eduS.append(str(edu.text.strip()))
            # print eduS
        certS=[]
        certfications=soup.find("section",attrs={'data-nav-waypoint':'experience'}).findNext("section").findNext("section")
        for cert in certfications.find_all("li"):
            remove_span=cert.find('span')
            remove_span.extract()
            certS.append(str(cert.text.strip()))
            # print certS
        doctorData={
            'name':name,
            'overview':overview,
            'practice_years':practiceYears,
            'language':language,
            'office_location':officeLocation,
            'hospital_affiliation':','.join(hostelAffi),
            'specification':','.join(specS),
            'sub_specification':','.join(subSpecs),
            'education':','.join(eduS),
            'certifications':','.join(certS),
        }
        doctorsData.append(doctorData)
    except Exception as e:
        print(str(e))

def writeData():
    # field names
    fields = ['name', 'overview', 'practice_years', 'language','office_location','hospital_affiliation','specification','sub_specification','education','certifications']
    try:
        with open('data.csv', 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.DictWriter(csvfile,fieldnames=fields)
            # writing headers (field names)
            csvwriter.writeheader()
            # writing data rows
            csvwriter.writerows(doctorsData)
    except Exception as e:
        print(str(e))
    print "yes"
getCities('NJ')
