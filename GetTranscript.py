import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
options.add_argument("--start-maximized")

year_list = ['2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
q_list = ['q1', 'q2', 'q2', 'q3']

def getTicker():
    ticker_list = []
    with open('Tickers.csv') as csv_file:
        next(csv_file) #Skip the first line because it is the header
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[2] not in ticker_list: # Check for tickers not in list, if not in list then we append (add)
                ticker_list.append(row[2])
                #print(row[2])
                with open("TickerList" + ".txt", "a", encoding="utf8") as output:
                    output.write('\n' + row[2])

#print(ticker_list) #Debug purpose only

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def scriptScraping():
    ticker = ''
    year = ''
    quarter = ''
    finalScript_list = [line.strip() for line in open('TranscriptFullList.txt')]
    driver = webdriver.Chrome(options = options)
    driver.get("https://seekingalpha.com/account/login")
    driver.find_element_by_name('email').click()
    driver.find_element_by_name('email').send_keys('EMAIL@GMAIL.COM') #Replace EMAIL@GMAIL.COM with your email address
    time.sleep(random.randint(1, 5))

    driver.find_element_by_name('password').click()
    driver.find_element_by_name('password').send_keys('PASSWORD') #Replace "PASSWORD" with your password
    time.sleep(random.randint(1, 5))

    driver.find_element_by_xpath('//*[@id="root"]/div[1]/main/div/form/button').click() #Sign-in button
    time.sleep(random.randint(1, 5))
    index = 0
    for link in finalScript_list:
        page = link.split('Link: ')[-1]
        index = index + 1
        print(index)
        driver.get(str(page))
        ticker = find_between(link, "Ticker: ", " | Year:")
        year = find_between(link, "Year: ", " | Quarter:")
        quarter = find_between(link, "Quarter: ", " - Link")
        body = driver.find_elements_by_class_name('sa-art')
        time.sleep(random.randint(1, 5))
        file_name = ticker + "_" + year + "_" + quarter
        dir = 'E:\\Learning Python\\Learning on my own\\Conference Call Transcript Scrape\\Transcripts\\'
        with open(dir + file_name + ".txt", "w", encoding="utf-8") as output:
            output.write("\n".join([post.text for post in body]))

def scroll_down(drv):
    # Get scroll height.
    last_height = drv.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height.
        new_height = drv.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height



#getTicker()
scriptScraping()
