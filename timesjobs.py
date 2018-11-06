import json
import requests
import time
import traceback


def addBlanks(row):
    for i in row:
        if row[i] is None:
            row[i] = ''


def scrape():
    timestamp = time.time()
    headers = json.load(open('headers.json'))
    json_filename = './files/timesjobs.json'
    fp = open(json_filename, 'w')

    url = 'https://jobbuzz.timesjobs.com/jobbuzz/loadMoreJobs.json?companyIds=&locationnames=198130$&aosValues=&sortby=Y&from=filter&faids=&txtKeywords=&pSize=50'
    response = requests.get(url)
    jobs = json.loads(response.text)
    jobs = jobs['jobsList']

    joblist = []
    for job in jobs:
        row = dict.fromkeys(headers)
        row['title'] = job['title']
        row['applylink'] = 'http://www.timesjobs.com/candidate/' + job['jdUrl']
        row['jd'] = job['jobDesc']
        row['companyname'] = job['companyName']
        row['location'] = job['Location']
        row['salary'] = job['salary']

        row['skills'] = ", ".join([x.strip().strip("\"") for x in job['keySkills']])

        row['enddate'] = job['expiry']

        row['source'] = 'timesjobs'
        row['experience'] = job['experience'] + " yrs"
        row['timestamp'] = timestamp
        addBlanks(row)
        print(row)
        joblist.append(row)

    json.dump(joblist, fp)
    fp.close()


try:
    scrape()
except Exception as ex:
    with open("error.log", 'a') as errorlog:
        #print(time.asctime() + ":" + ex, file=errorlog)
        traceback.print_exc(file=errorlog)
