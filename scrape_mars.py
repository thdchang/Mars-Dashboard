#dependencies to scrape the web to do analysis.
import pandas as pd
from bs4 import BeautifulSoup
import requests 
from splinter import Browser
from selenium import webdriver
import time

def scrape():
    
    #----------------------------------
    # # NASA Mars News
    #----------------------------------

    #mars news url
    url = "https://mars.nasa.gov/news/"

    #an instance of the chromedriver
    driver = webdriver.Chrome("C:/Users/tomhd/Desktop/USC Data Analytics/Homework/Mission_to_Mars/Mission-to-Mars/chromedriver.exe")
    driver.get(url);

    #get the page source of the mars news webpage
    html = driver.page_source


    #create BeautifulSoup instance of mars news html
    soup = BeautifulSoup(html,'html.parser')


    #extract parent element for latest article
    latest_article = soup.find("ul", class_="item_list").find("div", class_="list_text")


    #extract latest article text 
    latest_article_text = latest_article.find("a").text


    #extract latest article date
    latest_article_date = latest_article.find("div", class_="list_date").text


    #extract latest article paragraph
    latest_article_p = latest_article.find("div", class_="article_teaser_body").text


    #-----------------------------------
    # # JPL Mars Space Images - Featured Image
    #-----------------------------------


    #jpl featured space image url 
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    #navigate driver to JPL Mars Space Images website
    driver.get(jpl_url);

    #retrieve the page source of the JPL Mars Space Images - Featured Image webpage
    jpl_image_html = driver.page_source

    # #create an BeautifulSoup instance
    # jpl_image_soup = BeautifulSoup(html,'html.parser')

    # #extract the first li tag in the document
    # jpl_image_soup.find("li", class_="slide")

    #use selenium to navigate webpage
    element = driver.find_element_by_xpath("//a[@class='fancybox']")
    element.click()
    time.sleep(5)
    #navigate to the webpage that has the full size of the latest mars featured image
    element = driver.find_element_by_link_text('more info')
    element.click()

    #retrieve the page source of the next website
    jpl_image_html_2 = driver.page_source


    #get the latest jpl image html page
    jpl_image_soup_2 = BeautifulSoup(jpl_image_html_2,'html.parser')

    #extract the jpl image url
    jpl_image_end_url = jpl_image_soup_2.find("figure", class_="lede").find("img")['src']


    #jpl homepage
    jpl_start_url = "https://www.jpl.nasa.gov"

    #concatenate to get full url for the full size jpl latest image of mars
    jpl_image_full_size_url = jpl_start_url + jpl_image_end_url



    #---------------------------------
    # # Mars Weather
    #---------------------------------

    #mars weather twitter page url
    twitter_url = "https://twitter.com/marswxreport?lang=en"


    response = requests.get(twitter_url)


    #create beautiful soup object of twitter page
    twitter_soup = BeautifulSoup(response.text,'html.parser')


    #extract container containing tweets 
    a = twitter_soup.find("div", class_="stream")


    #extract the latest mars weather tweet
    latest_tweet = twitter_soup.find("div", class_="stream").find("div", class_="tweet").find("p", class_="tweet-text").text


    #-----------------------------------
    # # Mars Facts
    #-----------------------------------

    #url of mars facts homepage
    mars_facts_url = "https://space-facts.com/mars/"

    #find the tables in the mars facts homepage
    mars_facts_table = pd.read_html(mars_facts_url)

    #display extracted html table from mars facts homepage
    mars_facts_table

    #create and manipulate the dataframe of the mars facts
    df = mars_facts_table[0]
    df = df.set_index(0)
    df.index.name = 'Description'
    df.columns=["Value"]

    # Convert Dataframe to HTML table
    table_html = df.to_html()

    #clean the html format
    table_html.replace('\n', '')

    #export dataframe to table.html file
    df.to_html('table.html')


    #-------------------------------
    # # Mars Hemispheres
    #-------------------------------


    #maris hemisphere website url
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #navigate driver to Mars Hemispheres website
    driver.get(mars_hemisphere_url);

    #request server
    response = requests.get(mars_hemisphere_url)
    hemisphere_soup = BeautifulSoup(response.text, 'html.parser')

    #extract the list containing hemisphere image links to each of mars hemisphere's respective page
    hemisphere_results = hemisphere_soup.find_all("div", class_="item")

    #create an array to store hemisphere image_urls
    hemisphere_image_urls = []

    #for loop to retrieve the hemisphere image titles and urls
    for result in hemisphere_results:

        #declare hemisphere dictionary to store title and image url for each hemisphere
        hemisphere_dictionary = {}

        #extract the name of hemisphere
        hemisphere_name = result.find('h3').text
        
        #append key/value of unique hemisphere name to dictionary
        hemisphere_dictionary['title'] = hemisphere_name

        #navigate the hemisphere        
        element = driver.find_element_by_link_text(hemisphere_name)
        element.click()
        time.sleep(5)
        
        #retrieve current webpage's page source 
        mars_hemisphere_url_2 = driver.page_source
        
        #create BeautifulSoup object of the page source
        hemisphere_image_soup = BeautifulSoup(mars_hemisphere_url_2,'html.parser')
        
        #extract the image url of the current hemisphere webpage
        image_url = hemisphere_image_soup.find('div', class_="downloads").find('a')['href']
        
        #append key/value of hemiphere's image_url to hemisphere dictionary
        hemisphere_dictionary['img_url'] = image_url
        
        #append each unique mars hemisphere dictionaryto a list
        hemisphere_image_urls.append(hemisphere_dictionary)
        
        #return to previous page
        driver.back()


    #close browser after finishing scraping mars hemisphere image title and urls
    driver.quit()


    #web-scraped data:
    mars_data = {"mars_news":[latest_article_text,latest_article_date,latest_article_p] ,"jpl_featured_image_url":jpl_image_full_size_url, "weather_tweet":latest_tweet,"hemisphere_image":hemisphere_image_urls}
    
    return mars_data


