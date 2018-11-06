import json
import requests
import time
import traceback
from bs4 import BeautifulSoup


def addBlanks(row):
    for i in row:
        if row[i] is None:
            row[i] = ''


def scrape():
    timestamp = time.time()
    headers = json.load(open('headers.json'))
    json_filename = './files/myamcat.json'
    fp = open(json_filename, 'w')

    joblist = []
    for i in range(117, 120):
        url = 'https://www.myamcat.com/jobs-search-ajax?strEventID=1&strCompanyID=&strMinSalary=0&strMaxSalary=9900000&strStartLimit=0&strKeyword=&strAdvCategoryName=0&strAdvLocationID=0&strAdvSectorID=&strAdvFlagID=0&sortBy=2&strJobRolesList=&strCompaniesList=&strInvitedJobs=0&strFreeSearchText=0&strHeaderJobSearchLocation=&_=1524471212{}%20HTTP/1.1'.format(
            i)
        response = requests.get(url)
        jobs = json.loads(response.text)

        for job in jobs['1']:
            row = dict.fromkeys(headers)
            row['title'] = job['jobprofileName']
            row['applylink'] = 'https://www.myamcat.com' + job['jdLink']
            row['jd'] = [x for x in BeautifulSoup(job['description'], "lxml").stripped_strings][0].replace('\u00a0',
                                                                                                           ' ')
            row['companyname'] = job['companyName']
            row['location'] = job['cityName']
            row['experience'] = str(job['minJobEx']) + ' yrs'
            row['salary'] = job['salary']
            row['created'] = job['datePosted']
            row['source'] = 'amcat'
            row['timestamp'] = timestamp
            addBlanks(row)
            print(row)
            joblist.append(row)

    json.dump(joblist, fp, indent=1)
    fp.close()


try:
    scrape()
except Exception as ex:
    with open("error.log", 'a') as errorlog:
        # print(time.asctime() + ":" + ex, file=errorlog)
        traceback.print_exc(file=errorlog)
