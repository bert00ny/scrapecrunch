#I believe a VPN with numerous dynamic IP addresses is needed to use this script to quickly scrape websites
# Only a few pages are missing from Google cache, those websites can be scraped seperately from the actual website
# data from Google cache is printed in terminal (for now); however, logo and description are saved to text file

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen, Request
from fake_useragent import UserAgent
import webbrowser

import time
from datetime import datetime

import pyautogui as py
import regex as re


class CrunchbaseScraper:
    def scraper(self):
        # load chrome webdriver
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        opts = Options()

        #use fakeuseragent to convince google that I am a different user each time
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        opts.add_argument(f'user-agent={userAgent}')     
        driver = webdriver.Chrome(options=opts)
        
        #open link to website
        driver.get(self.link)
        time.sleep(10)
        
        #get company name, if captcha appears script is paused until captcha is solved
        try:
            name = driver.find_element_by_xpath(self.name).text
        except:
            wait = input("Press Enter to continue.")
            print(wait)
            time.sleep(6)
            try:
                driver.get(self.link)
            except:
                pass


        #scrape data for name, about company, location, company size, company website, when it was founded
        # funding received, relevant industries, legal name, link to financial data, and social media      
        try:
            name = driver.find_element_by_xpath(self.name).text    
            about = driver.find_element_by_xpath(self.about).text
            time.sleep(1)
            location = driver.find_element_by_xpath(self.location).text
            size = driver.find_element_by_xpath(self.size).text
            time.sleep(1)
            website = driver.find_element_by_xpath(self.website).text
            founded = driver.find_element_by_xpath(self.founded).text
            funding = driver.find_element_by_xpath(self.funding).text
            print(name + '\n', about + '\n', location + '\n', size + '\n', website + '\n', founded + '\n', funding + '\n')
            industries = driver.find_elements_by_xpath(self.industries)
            for elem in industries:
                print(elem.text)

            legalname = driver.find_elements_by_xpath(self.legalname)
            for info in legalname:
                print(info.text)


                time.sleep(5)

            financials = driver.find_element_by_xpath(self.financials)

        
            value = financials.get_attribute("href")
            
            social = driver.find_elements_by_xpath(self.social)
            for soc in social:
                account = soc.get_attribute("href")
                print(account)
        except:
            pass
        
        #close current webpage and go to page with financial data
        driver.quit()
        time.sleep(5)
        driver = webdriver.Chrome(chrome_options=opts) 
        opts = Options()

        #restart fakeuseragent
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        opts.add_argument(f'user-agent={userAgent}')
        
        #open link with financial data 
        try:
            driver.get('http://webcache.googleusercontent.com/search?q=cache:' + str(value))
        except:
            pass
        time.sleep(10)

        #test if webpage for financial data exists in Google cache or stop if captcha appears
        try:
            transactions = driver.find_elements_by_xpath(self.transactions)
        except:
            wait = input("Press Enter to continue.")
            print(wait)
            time.sleep(6)
            try:
                driver.get(self.link)
            except:
                pass
        
        #get data for first transaction/date of transaction if it exists
        try:
            transactions = driver.find_elements_by_xpath(self.transactions)
            first = transactions[0].text
        
            firsttext = str(first)
            removecompany = firsttext.replace(str("- " + name), '')
            print(removecompany)

            mostrecent = driver.find_elements_by_xpath(self.datetime)

            firstdate = mostrecent[0].text
            print(firstdate)
            firstdate = str(firstdate)
            firstdate = firstdate.replace(',', '')
            datetime_object = datetime.strptime(str(firstdate), '%b %d %Y')
            datetime_object = datetime.strptime(str(firstdate), '%Y')
            datetime_object = datetime.strptime(str(firstdate), '%d %Y')
            datetime_object = datetime.strptime(str(firstdate), '%b %Y')

            timestamps = datetime.timestamp(datetime_object)
            print("timestamp =", timestamps)
            driver.quit()

            time.sleep(10)
        except:
            pass

#open csv file to links
with open('/home/tbert/Documents/Job search/Eutopia/linkseutopia.csv', 'rt') as links_csv:
    for linky in links_csv:
        scrape1 = CrunchbaseScraper()
        #scrape1.link = "https://www.crunchbase.com/organization/climeon"
        scrape1.link = "http://webcache.googleusercontent.com/search?q=cache:" + linky

        #Xpath for all relevant data
        scrape1.name = "//h1[@class='profile-name']"
        scrape1.about = "//span[@class='description']"
        scrape1.location = "//a[@class='link-accent ng-star-inserted']"
        scrape1.size = "//a[@class='component--field-formatter field-type-enum link-accent ng-star-inserted']"
        scrape1.website = "//a[@class='component--field-formatter link-accent ng-star-inserted']"
        scrape1.industries = "//div[@class='cb-overflow-ellipsis']"
        scrape1.founded = "//span[@class='component--field-formatter field-type-date_precision ng-star-inserted']"
        scrape1.legalname = "//span[@class='ng-star-inserted']"
        scrape1.description = "//span[@class='description has-overflow']"
        scrape1.funding = "//span[@class='component--field-formatter field-type-money ng-star-inserted']"
        scrape1.social = "//a[@class='component--field-formatter icon-only link-primary ng-star-inserted']"
        scrape1.button = '//button[contains(., "Read More")]'
        scrape1.financials = '//a[contains(., "Financials")]'
        scrape1.transactions = '//div[@class="identifier-label"]'
        scrape1.datetime = '//span[@class="component--field-formatter field-type-date ng-star-inserted"]'
        
        #start scraping all the data
        scrape1.scraper()

        #get description of company, button to open description does not work in Google cache
        #instead requests is used to get the text file of the html code, afterwhich description is extracted using regex
        
        r = Request(linky, headers={'User-Agent': 'Mozilla/5.0'})

        #clean link address for the purpose of naming individual output files
        linky = str(linky)
        linky2 = linky.replace("https://www.crunchbase.com/organization/", '')
        linky2 = linky2.replace("\n", '')

        f = open(linky2 + ".txt", "w")
        page = urlopen(r).read()
        f.write(str(page))
        f.close()
        
        #open html data and clean data
        #the second result1 re.search is missing data cleansing process (for now)
        with open(linky2 + ".txt", "r") as e, open(linky2 + 'CLEAN.txt', 'a+') as k:
            content = e.read()
            content = str(content)
            result1 = re.search('(class="description has-overflow")(.*)(<button _ngcontent-)', content)
            result1 = re.search('(class="description")(.*)(</description-card>)', content)

            result1 = str(result1)

            result1 = result1.replace(')', "")
            result1 = result1.replace('(', "")
            result1 = result1.replace("'", "")
            result1 = result1.replace('"', "")
            result1 = result1.replace('\\', "")
    
            result1 = re.sub('<regex.Match object; span=', '', str(result1))
            result1 = re.sub(r'\d{1,10}\, \d{1,10}', '', str(result1))
            result1 = re.sub(r', match=class=description has-overflow><p>', '', str(result1))
            result1 = re.sub(r'\w+\d+\w+', '', str(result1))
            result1 = re.sub(r'<.*?>', '', str(result1))
    
    
            k.write(str(result1))
    
        #take a screenshot of company logo, company logo is missing in Google cache
        #screenshot is take with standar webbrowser and pyautogui
        webbrowser.open(linky)

        time.sleep(5)

        py.screenshot(linky2 + "PIC.png", region=(673, 195, 164, 164))

        time.sleep(10)

        #in order to take a screenshot the mouse coordinates are taken and inserted into region=(x, y, c, d))
        # x = x value of upper left corner of image, y = y value of upper left corner of image
        # c = width of image, d = height of image
        # the code for getting the coordinates should be run seperately and is as follows:
        # import pyautogui as py #Import pyautogui
        #import time
        # while True:
        #   print(py.position())
        #    time.sleep(1)




