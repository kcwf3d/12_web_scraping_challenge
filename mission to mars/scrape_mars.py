from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def inital_browser():
    executable_path = {"executable_path": "C:\\Users\kcwf3\DataBootCamp\chromedriver"}
    browser=Browser("chrome", **executable_path, headless=False)

#scraping dictionary for mongo
mars_data={}

def news_scrape():
    browser= inital_browser() 
    url = " https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    #html and soup def
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #slide element
    slide_elem = soup.select_one('div.list_text')

    #news article title
    art_title=slide_elem.find("div", class_="content_title").get_text()

    #news article body
    art_body=slide_elem.find("div", class_="article_teaser_body").get_text()

    #Mars News Diction
    mars_data['article_title']=art_title
    mars_data['article_body']=art_body

    return mars_data

    browser.quit()

def scrape_images():
    browser = inital_browser()

    base_url= "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(base_url)
    #html and soup def
    html_image = browser.html
    soup = BeautifulSoup(html_image, "html.parser") 

    image_url=soup.find("a", class_ = "showimg fancybox-thumbs")["href"]
    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url}"
    browser.quit()

    return mars_data

def scrape_mars_facts():
    browser = inital_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    table = pd.read_html(facts_url)

    facts_df = table[0]
    facts_df.columns = ['Mars Facts', 'Info']
    facts_df['Mars Facts'] = facts_df['Mars Facts'].str.replace(':', '')

    facts_html = facts_df.to_html()
    
    mars_data['table']= facts_html

    return mars_data

def scrape_mars_hemispheres():

    # Initialize browser 
    browser = inital_browser()

    hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    base_url="https://astrogeology.usgs.gov"

    #loop
    items = soup.find_all('div', class_='item')
    #making a loop to find image url
    img_url=[]
    for i in items:
        title = i.find('h3').text
        hem_image_url= i.find('a',class_='itemLink product-item')['href']
        browser.visit(base_url + hem_image_url)
        hem_image_url =browser.html
        soup= BeautifulSoup(hem_image_url,'html.parser')
        image_link= base_url + soup.find('img',class_='wide-image')['src']
        img_url.append({'title': title, 'img_url':image_link})
    
    mars_data['hemisphere url'] =img_url

    browser.quit()

    return mars_data
    