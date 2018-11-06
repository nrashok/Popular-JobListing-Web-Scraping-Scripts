import json
import time
import traceback
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def addBlanks(row):
    for i in row:
        if row[i] is None:
            row[i] = ''


def scrape():
    timestamp = time.time()
    headers = json.load(open('headers.json'))
    filename = "./files/internshala.json"
    fp = open(filename, "w")
    joblist = []
    for i in range(0, 3):
        my_url = 'https://internshala.com/internships/internship-in-bangalore/page-{}'.format(i)
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("div", {"class": "container-fluid individual_internship "})
        for container in containers:
            row = dict.fromkeys(headers)
            row['title'] = container.a.text
            row['applylink'] = 'https://internshala.com' + container.a["href"]
            company_container = container.findAll("a", {"class": "link_display_like_text"})
            row['companyname'] = company_container[0].text
            location_container = container.findAll("a", {"class": "location_link"})
            row['location'] = location_container[0].text
            stipend_container = container.findAll("td", {"class": "stipend_container_table_cell"})
            row['salary'] = stipend_container[0].text
            type_container = container.findAll("div", {"class": "button_container"})
            row['type'] = " ".join(type_container[0].div.text.split())
            start_container = container.findAll("div", {"id": "start-date-first"})
            row['startdate'] = start_container[0].text
            apply_by_container = container.findAll("div", {"class": "table-responsive"})
            apply_by = apply_by_container[0].findAll("td")
            row['enddate'] = apply_by[4].text
            posted_on_container = container.findAll("div", {"class": "table-responsive"})
            posted_on = posted_on_container[0].findAll("td")
            row['created'] = posted_on[3].text
            row['source'] = 'internshala'
            row['experience'] = 'Fresher'
            row['location'] = 'Bengaluru'
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
