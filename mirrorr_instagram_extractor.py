from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import requests, re, json ,pprint
import urllib
import urllib.request
from selenium.webdriver.common.keys import Keys
from IPython.display import Image


def load_profile_page(userid,driver_path='./chromedriver'):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   
    main_driver = webdriver.Chrome(driver_path,options=options)
    main_driver.implicitly_wait(10)
    main_driver.get("https://www.instagram.com/"+userid)
    return main_driver

def extract_profile_pic_uri (main_driver):
    pic_url = main_driver.find_element_by_class_name(name='_6q-tv')
    return pic_url.get_attribute(name='src')
    
def extract_followers(main_driver):
    follower_element =  main_driver.find_element_by_partial_link_text(link_text="followers")
    return follower_element.find_element_by_class_name(name='g47SY').text

def extract_post_count(main_driver):
    follower_element = main_driver.find_element_by_partial_link_text(link_text="posts")
    return follower_element.find_element_by_class_name(name='g47SY').text

def extract_following(main_driver):
    follower_element = main_driver.find_element_by_partial_link_text(link_text="following")
    return follower_element.find_element_by_class_name(name='g47SY').text

def download_profile_pic(userid,output_path='./'):
    main_driver = load_profile_page(userid=userid)
    profile_pic_uri = extract_profile_pic_uri(main_driver)
    urllib.request.urlretrieve(profile_pic_uri,output_path+userid+'.jpg')
    
class InstaUser:
    def __init__(self,userid):
        self.main_driver = None
        self.userid = userid
        self.profile_pic_uri = None
        self.followers = None
        self.following = None
        self.post_count = None
        self.profile_thumbnail = None
        self.screenshot = None
        self.fileout = None
        self.axn = None
        self.init_driver()
    def init_driver(self):
        self.main_driver = load_profile_page(userid=self.userid)
        self.axn = ActionChains(self.main_driver)
    # Profile Page Info
    def extract_follower(self):
        self.followers = extract_followers(self.main_driver)
    def extract_following(self):
        self.following = extract_following(self.main_driver)
    def extract_post_count(self):
        self.post_count = extract_post_count(self.main_driver)        
    def extract_profile_infos(self):
        self.extract_follower()
        self.extract_following()
        self.extract_post_count()
        self.extract_profile_pic_uri()
    
    #   Pics  
    def extract_profile_pic_uri(self):
        self.profile_pic_uri = extract_profile_pic_uri(self.main_driver)
    #  def extract_first_pic_uri(self):
    #  extract first pic
                
    # Do something
    
    def scroll_down_page(self):
        self.axn.send_keys(Keys.END).perform()    
        
    # Outputs        
    def screenshot_main(self,fileout='main-page.png'):
        self.main_driver.get_screenshot_as_file(fileout)
        self.fileout=fileout
        
    def to_csv(self, csvfile):
        print(csvfile)
        
    def to_db(self, db_host, db_password, db_table):
        print('write to db')    