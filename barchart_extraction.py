from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import re, json ,pprint
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import urllib.request
from selenium.webdriver.common.keys import Keys
from IPython.display import Image
from urllib.parse import urlparse
from time import sleep
import datetime
import pytz # new import
import csv

from dateparser.search import search_dates
import arrow
import datetime
from dateutil.parser import parse
import weasyprint 
from google.cloud import storage

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))
    except:
        print('File not available')
        
def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
    
def update_file(bucket_name,name,pdf_filename):
    download_blob(bucket_name='brextract', 
                  source_blob_name='csv/'+ name + '.csv',
                  destination_file_name= name + '.csv')

    upload_blob(bucket_name='brextract', 
                source_file_name= name + '.csv', 
                destination_blob_name='csv/'+ name + '.csv')  
    upload_blob(bucket_name='brextract', 
                source_file_name=pdf_filename, 
                destination_blob_name='screenshots/'+name + '/' + pdf_filename)      

    
def get_capture_timestamp():
    return datetime.datetime.now()
def get_capture_date(timestamp):
    return timestamp.strftime("%a %b %d, %Y")
def get_capture_time(timestamp,timezone=pytz.UTC):
    return timestamp.astimezone(pytz.UTC).strftime("%H:%M:%S %Z")
def get_capture_time_filename(timestamp,timezone=pytz.UTC):
    return timestamp.astimezone(pytz.UTC).strftime("%Y-%m-%d_%H-%M-%S-%Z")

def extract_last(webdriver):
    iv = webdriver.find_element_by_class_name(name='pricechangerow')
    return iv.find_element_by_xpath("//span[@class='last-change']").text

def extract_days_to_expiration(webdriver):
    dt_expiration = webdriver.find_element_by_class_name(name='bc-options-toolbar__second-row')
    a = dt_expiration.find_element_by_xpath("//strong[contains(text(), 'Days')]")
    
    out = re.match(string=a.text,pattern='^([0-9]+)')
    return out.group(1)

def screenshot_page(webdriver,output_file='out.pdf'):
    page = webdriver.page_source
    weasyprint.HTML(file_obj=page).write_pdf(output_file)
    
def load_site(driver_path='./chromedriver',input_url= 'https://www.barchart.com/futures/quotes/ZW*0/options?futuresOptionsView=split'):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    driver = webdriver.Chrome(driver_path,options=options)
    driver.implicitly_wait(10)    
    driver.get(input_url)
    sleep(1)
    return driver

def extract_left_strike(webdriver):
    lp_left = webdriver.find_elements_by_xpath("//td[@class='lastPrice_left']")
    strike_price = webdriver.find_elements_by_xpath("//td[@class='strikePrice']")
    lp_right = webdriver.find_elements_by_xpath("//td[@class='lastPrice_right']")
    out_list = []
    for i in range(len(lp_left)):
        out_list.append([lp_left[i].text,strike_price[i].text,lp_right[i].text])
    return out_list
def extract_iv(webdriver):
    iv = webdriver.find_element_by_class_name(name='bc-options-toolbar__second-row')
    a = iv.find_element_by_xpath("//div[contains(text(), 'Implied Volatility')]/strong")
    return a.text

def extract_barchart_site(input_url='https://www.barchart.com/futures/quotes/ZW*0/options?futuresOptionsView=split'\
                         ,name='wheat',write_option='a'):
    print("url is: " + input_url)
    capture_timestamp = get_capture_timestamp()
    capture_date = get_capture_date(timestamp=capture_timestamp)
    capture_time = get_capture_time(timestamp=capture_timestamp)
    capture_stamp = get_capture_time_filename(timestamp=capture_timestamp)    
    driver = load_site(input_url=input_url)
    
    output_file = name + ".csv"    
    output_screenshot = name+'_'+capture_stamp+'.pdf'
    test_out = extract_left_strike(webdriver=driver)

    download_blob(bucket_name='brextract', 
                  source_blob_name='csv/'+ output_file,
                  destination_file_name= output_file)
    
    with open(output_file, write_option) as csvfile:
        writer = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["Date",capture_date])
        writer.writerow(["Last",extract_last(webdriver=driver)])
        writer.writerow(["Days to expiration",extract_days_to_expiration(webdriver=driver)])
        writer.writerow(["IV",extract_iv(webdriver=driver)])
        writer.writerow(["Time",capture_time])
        writer.writerow([])
        writer.writerow(["Last","Strike","Last"])
        for i in test_out:
            if(i[0]=='Last'):
                continue
            writer.writerow(i)
            
        writer.writerow([])
        screenshot_page(webdriver=driver,output_file=output_screenshot)
        
    upload_blob(bucket_name='brextract', 
                source_file_name= output_file, 
                destination_blob_name='csv/'+ output_file)  
    upload_blob(bucket_name='brextract', 
                source_file_name=output_screenshot, 
                destination_blob_name='screenshots/'+name + '/' + output_screenshot)      
    print('Successfully uploaded code uri')

def extract_barchart_code(input_code='ZW*0'\
                         ,name='wheat',write_option='a'):
    input_url='https://www.barchart.com/futures/quotes/' + input_code + '/options?futuresOptionsView=split'    
    capture_timestamp = get_capture_timestamp()
    capture_date = get_capture_date(timestamp=capture_timestamp)
    capture_time = get_capture_time(timestamp=capture_timestamp)
    capture_stamp = get_capture_time_filename(timestamp=capture_timestamp)    
    driver = load_site(input_url=input_url)
    
    output_file = name + ".csv"    
    output_screenshot = name+'_'+capture_stamp+'.pdf'

    test_out = extract_left_strike(webdriver=driver)
    
    download_blob(bucket_name='brextract', 
                  source_blob_name='csv/'+ output_file,
                  destination_file_name= output_file)
    
    with open(output_file, write_option) as csvfile:
        writer = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["Date",capture_date])
        writer.writerow(["Last",extract_last(webdriver=driver)])
        writer.writerow(["Days to expiration",extract_days_to_expiration(webdriver=driver)])
        writer.writerow(["IV",extract_iv(webdriver=driver)])
        writer.writerow(["Time",capture_time])
        writer.writerow([])
        writer.writerow(["Last","Strike","Last"])
        for i in test_out:
            if(i[0]=='Last'):
                continue
            writer.writerow(i)
            
        writer.writerow([])
        screenshot_page(webdriver=driver,output_file=output_screenshot)
        
    upload_blob(bucket_name='brextract', 
                source_file_name= output_file, 
                destination_blob_name='csv/'+ output_file)  
    upload_blob(bucket_name='brextract', 
                source_file_name=output_screenshot, 
                destination_blob_name='screenshots/'+name + '/' + output_screenshot)            
    print('Successfully uploaded code workflow')