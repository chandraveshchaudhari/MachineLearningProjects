import csv
import time
from bs4 import BeautifulSoup
import sys, io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import *

no_of_reviews = 1000

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# download chromedriver from http://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(r"/home/chaudharyubuntu/Downloads/chromedriver_linux64(1)/chromedriver")

wait = WebDriverWait( driver, 10 )


# Append all of google Play store urls here
urls = ["https://play.google.com/store/apps/details?id=com.outfit7.mytalkingtom2&hl=en"]

for url in urls:

    driver.get(url)

    page = driver.page_source

    soup_page = BeautifulSoup(page, "html.parser")

    soup_table = soup_page.find("h1", class_="AHFaub")

    #print("App name: ", soup_table.string)

    soup_table = soup_page.findAll("span", class_="htlgb")[4]

    #print("Installs Range: ", soup_table.string)
    '''
   # soup_table = soup_page.find("meta", itemprop="ratingValue")

   # print("Rating Value: ", soup_table['content'])

   # soup_table = soup_page.find("meta", itemprop="reviewCount")

   # print("Reviews Count: ", soup_table['content'])
    '''

    soup_histogram = soup_page.find("div", class_="VEF2C")

    rating_bars = soup_histogram.find_all('div', class_="mMF0fd")
    '''
    for rating_bar in rating_bars:
        print("Rating: ", rating_bar.find("span").text)
        print("Rating count: ", rating_bar.find("span", class_="L2o20d").get('title'))
    '''
    # open all reviews
    url = url+'&showAllReviews=true'
    driver.get(url)
    time.sleep(5) # wait dom ready
    # scrolling code
    for i in range(1,10):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')#scroll to load other reviews
        time.sleep(1)
    page = driver.page_source

    soup_page = BeautifulSoup(page, "html.parser")
    expand_pages = soup_page.findAll("div", class_="d15Mdf")
    counter = 1
    one=[]
    five = []
    for expand_page in expand_pages:
        try:
            #print("\n===========\n")
            #print("review："+str(counter))
            #print("Author Name: ", str(expand_page.find("span", class_="X43Kjb").text))
            #print("Review Date: ", expand_page.find("span", class_="p2TkOb").text)
            '''
            //didn't find reviewer link
            print("Reviewer Link: ", expand_page.find("a", class_="reviews-permalink")['href'])
            '''
            reviewer_ratings = expand_page.find("div", class_="pf5lIe").find_next()['aria-label'];
            reviewer_ratings = reviewer_ratings.split('(')[0]
            reviewer_ratings = ''.join(x for x in reviewer_ratings if x.isdigit())
            #print("Reviewer Ratings: ", reviewer_ratings)
            
            
            if reviewer_ratings == '1':
                one.append(str(expand_page.find("div", class_="UD7Dzf").text))
            elif reviewer_ratings == '5':
                five.append(str(expand_page.find("div", class_="UD7Dzf").text))
            else:
                pass
                
            
            '''
            //didn't find review title
            print("Review Title: ", str(expand_page.find("span", class_="review-title").string))
            '''
            #print("Review Body: ", str(expand_page.find("div", class_="UD7Dzf").text))
            '''
            developer_reply = expand_page.find_parent().find("div", class_="LVQB0b")
            if hasattr(developer_reply, "text"):
                print("Developer Reply: "+"\n", str(developer_reply.text))
            else:
                print("Developer Reply: ", "")
            '''
            counter+=1
        except:
            pass
    
driver.quit()
       
    
def list_to_csv(csvfile, listname):
    '''
    csvfile: .csv data file location for saving
    listname: list from which to make .csv
    '''
    #Assuming it is a flat list
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in listname:
            writer.writerow([val])

list_to_csv("/home/chaudharyubuntu/Desktop/word_clouds_webScraping/one.csv", one)  
list_to_csv("/home/chaudharyubuntu/Desktop/word_clouds_webScraping/five.csv", five) 