import json
import time
import traceback
from html import unescape

import requests
from bs4 import BeautifulSoup


def addBlanks(row):
    for i in row:
        if row[i] is None:
            row[i] = ''
        elif type(row[i]) is str and i != 'applylink':
            row[i] = unescape(row[i].replace('\n', ' ').strip())


def scrape():
    timestamp = time.time()
    headers = json.load(open('headers.json'))
    json_filename = './files/jobguru.json'
    fp = open(json_filename, 'w')

    url = 'https://www.jobguru.in/jobs_response.php'
    response = requests.get(url)
    jobs = json.loads(response.text)
    jobs = jobs['jobs']

    joblist = []
    for job in jobs:
        row = dict.fromkeys(headers)
        row['title'] = [x for x in BeautifulSoup(job['title'], "lxml").stripped_strings][0]
        row['applylink'] = 'https://www.jobguru.in/job/' + job['id'] + '/' + job['slug']
        row['jd'] = job['description'].lstrip('Job Description')
        row['companyname'] = job['company']
        row['location'] = job['locations']
        row['salary'] = job['salary']
        row['type'] = job['shift']

        row['startdate'] = job['date']

        row['source'] = 'jobguru'
        row['experience'] = ''
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
