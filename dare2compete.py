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
    json_filename = './files/dare2compete.json'
    fp = open(json_filename, 'w')

    url = 'https://api.dare2compete.com/api/opportunity/search?opportunity=internships&sort=latest&page=1%20HTTP/1.1'
    response = requests.get(url)
    jobs = json.loads(response.text)
    jobs = jobs['data']['data']
    joblist = []
    for job in jobs:
        row = dict.fromkeys(headers)
        row['title'] = job['title']
        row['applylink'] = 'https://dare2compete.com/' + str(job['public_url'])
        row['jd'] = [x for x in BeautifulSoup(job['details'], "lxml").stripped_strings][0]
        row['location'] = job['location']
        row['type'] = job['type']
        row['startdate'] = job['start_date']
        row['enddate'] = job['end_date']
        row['created'] = job['display_date']
        row['source'] = 'dare2compete'
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
