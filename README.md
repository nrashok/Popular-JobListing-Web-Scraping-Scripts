#  Web scrapping scripts to collect and parse out job posting information for you!!

*I wanted to explore data science-related jobs posted to a variety of roles on job listing sites, a job aggregator that updates multiple times daily.*


### Job Listing/Postings Sites

| WebSite | URL | pyscript  |
| ------ | ------ | ----- |
| Aasaanjobs | https://www.aasaanjobs.com/| aasaanjobs.py 
| Dare2compete | https://dare2compete.com/ | dare2compete.py 
| Freshersworld | https://www.freshersworld.com/ | freshersworld.py
| Internshala | https://internshala.com/ | internshala.py
| Jobguru | https://www.jobguru.in/ | jobguru.py
| Myamcat | https://www.myamcat.com/jobs | myamcat.py 
| Timesjobs| https://www.timesjobs.com | timesjobs.py 
| Naukri | https://www.naukri.com | naukri.py 
| Shine | https://www.shine.com | shine.py 


### Installation

Install the python dependencies/pip modules to start the scrape.

```sh
$ pip install beautifulsoup4

$ pip install html5lib

$ pip install lxml

$ pip install pandas

```
A disclaimer before beginning, many websites can restrict or outright bar scraping of data from their pages.
Users may be subject to legal ramifications depending on where and how they attempt to scrape information.
Many sites have a devoted page to noting restrictions on data scraping at [example-site].com/robots.txt. 

[Scrape carefully, friends]
