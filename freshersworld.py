import json
import time
import traceback
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup


def addBlanks(row):
    for i in row:
        if row[i] is None:
            row[i] = ''


def scrape():
    timestamp = time.time()
    headers = json.load(open('headers.json'))
    json_filename = './files/freshersworld.json'
    fp = open(json_filename, 'w')

    joblist = []
    my_url = 'https://www.freshersworld.com/jobs/jobsearch?&limit=50'

    # to test connection
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    # saving pagename
    page_soup = soup(page_html, "html.parser")

    # to extract all div
    containers = page_soup.findAll("div", {
        "class": "col-md-12 col-lg-12 col-xs-12 padding-none job-container jobs-on-hover top_space"})
    len(containers)

    # to extract one container
    container = containers[0]
    len(container)

    for container in containers:
        row = dict.fromkeys(headers)

        # title
        job_role_container = container.findAll("div")
        job_role = job_role_container[4].text.strip()
        row['title'] = job_role.title()

        # applylink
        href = container.a["href"]
        row['applylink'] = href

        # jd
        description_container = container.findAll("span", {"class": "desc"})
        description = description_container[0].text.strip()
        row['jd'] = description.replace('\u00a0', " ")

        # companyname
        title = container.h3.text
        row['companyname'] = title

        # location
        location_container = container.findAll("span", {"class": "job-location display-block modal-open"})
        location = location_container[0].text.strip()
        row['location'] = location

        # skills
        qualification_container = container.findAll("span", {"itemprop": "qualifications"})
        qualification = qualification_container[0].text.strip()
        row['skills'] = qualification

        # enddate
        last_date_container = container.findAll("span", {"itemprop": "datePosted"})
        last_date = last_date_container[0].text.strip()
        row['enddate'] = last_date

        # posted_on
        posted_on_container = container.findAll("span", {"class": "ago-text"})
        posted_on = posted_on_container[0].text.strip()
        row['created'] = posted_on
        row['source'] = 'freshersworld'
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
