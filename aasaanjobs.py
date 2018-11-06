import json
import time
import traceback
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as soup


def addBlanks(row):
    for i in row:
        if row[i] is None:
            row[i] = ''


def scrape():
    timestamp = time.time()
    headers = json.load(open('headers.json'))
    json_filename = './files/aasaanjobs.json'
    fp = open(json_filename, 'w')

    joblist = []

    req = Request('https://www.aasaanjobs.com/s/bangalore-jobs-in-bengaluru/', headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    containers = page_soup.findAll("div", {
        'class': 'row p-top-sm card-custom pos-relative search-highlight search-card cursor-pointer track-search-click'})

    for container in containers:
        row = dict.fromkeys(headers)

        # title
        title = container.find("span", {'itemprop': 'title'}).text
        row['title'] = title.title()

        # applylink
        href = container.a["href"]
        row['applylink'] = 'https://www.aasaanjobs.com' + href

        # jd
        description = container.find("span", {'class': 'text-gray-lighter text-normal'}).text
        row['jd'] = description

        # companyname
        company = container.find("a", {
            'class': 'track-clevertap js-no-action text-capitalize text-primary text-semibold track-search-click'}).text
        row['companyname'] = company

        # location
        location = container.find("span", {'class': 'text-light'}).text
        row['location'] = location

        # experience
        qualification = container.find("div", {'class': 'col-xs-12 col-md-6 text-small text-light p-right-0'})
        experience = qualification.find("span", {'class': 'm-bottom-0 text-small'}).text
        row['experience'] = experience

        # salary
        salary = container.find("span", {'class': 'text-semibold'}).text.strip()
        row['salary'] = salary.lstrip('\u20b9')

        # type
        qualification = container.find("div", {'class': 'col-xs-12 col-md-6 text-small text-light p-right-0'})
        jobtype = qualification.find("p", {'class': 'm-bottom-0 text-small'}).text
        row['skills'] = jobtype

        # skills
        # startdate
        # enddate
        # created
        # source
        row['source'] = 'aasaanjobs'
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
