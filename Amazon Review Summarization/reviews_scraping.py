#Selectorlib, to extract data using the YAML file we created from the webpages we download
from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser
import xlsxwriter
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    #to make requests and download the HTML content of the pages
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)
product_title=""
complete_reviews=""
row_no=1
col_no=1
workbook = xlsxwriter.Workbook('reviews.xlsx')
sheet = workbook.add_worksheet()
sheet.write(0, 0, "Product_Name")
sheet.write(0, 1, "Review")
with open("urls.txt",'r') as urllist:
    for url in urllist.readlines():
        data = scrape(url)
        product_title = str(data["product_title"])
        sheet.write(1, 0, product_title)
        if data:
            for review in data['reviews']:
                complete_reviews+=str(review['content'])+" "
                sheet.write(row_no,col_no,review['content'])
                row_no+=1
# sheet.write('A2', product_title)
# sheet.write('B2', complete_reviews)

workbook.close()


    