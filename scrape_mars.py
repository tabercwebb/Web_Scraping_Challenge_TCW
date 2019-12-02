# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# Set Executable Path & Initialize Chrome Browser
def init_browser(): 
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create Empty Scrape Results Dictionary
    mars_scrape_results = {}

    ######## Mars News ########

   # Visit the NASA Mars News Site
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)

    # Pause to Load Webpage
    sleep(2)

    # Create BeautifulSoup Object & Parse with 'html.parser'
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the First News Article Title & Store in Scrape Results Dictionary
    mars_first_title = mars_news_soup.find('div', class_='content_title').text
    mars_scrape_results['news_title'] = mars_first_title

    # Scrape the First News Article Paragraph & Store in Scrape Results Dictionary
    mars_first_paragraph = mars_news_soup.find('div', class_='article_teaser_body').text
    mars_scrape_results['news_paragraph'] = mars_first_paragraph
  
    ######## Mars Featured Image ########

    # Visit the JPL Mars Space Images Site
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Pause to Load Webpage
    sleep(2)

    # Use Splinter to Navigate the Site
    full_image_link = browser.find_by_id('full_image')
    full_image_link.click()

    # Pause to Load Webpage
    sleep(2)

    # Use Splinter to Navigate the Site
    browser.click_link_by_partial_text('more info')

    # Pause to Load Webpage
    sleep(2)

    # Create BeautifulSoup Object & Parse with 'html.parser'
    html = browser.html
    featured_image_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the Full Image URL & Store in Scrape Results Dictionary
    featured_image_url = featured_image_soup.find('figure', class_='lede').a['href']
    featured_image_complete_url = f'https://www.jpl.nasa.gov{featured_image_url}'
    mars_scrape_results['featured_image'] = featured_image_complete_url
    
    ######## Mars Weather ########

    # Visit the Mars Weather Twitter Account
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # Pause to Load Webpage
    sleep(2)

    # Create BeautifulSoup Object & Parse with 'html.parser'
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')

    # Scrape Mars Weather Info & Store in Scrape Results Dictionary
    mars_weather = tweet_soup.find('p', class_='tweet-text').text
    mars_scrape_results['weather'] = mars_weather

    ######## Mars Facts ########

    # Visit the Mars Facts Webpage
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)

    # Pause to Load Webpage
    sleep(2)

    # Scrape the Mars Facts Table & Set Columns
    mars_facts = tables[0]
    mars_facts.columns = ['property', 'value']

    # Set Index
    mars_facts.set_index('property', inplace=True)

    # Convert DataFrame to HTML Table String
    mars_facts_html_table = mars_facts.to_html()

    # Store Mars Facts in Scrape Results Dictionary
    mars_scrape_results['facts'] = mars_facts_html_table

    ######## Mars Hemispheres ########

    # Visit the USGS Astrogeology Web Archive Site
    hemi_img_url = "https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_img_url)

    # Pause to Load Webpage
    sleep(2)

    # Create BeautifulSoup Object & Parse with 'html.parser'
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')

    # Create an Empty List and Append with Links For Each Hemisphere
    hemi_links = []
    links = hemi_soup.find_all('h3')

    # Loop Through Links to Get URL For Each
    for hemi in links:      
        hemi_links.append(hemi.text)
        
    # Create an Empty List and Append with Hemisphere_Image_URLs
    hemi_image_urls = []

    # Loop Through Hemi_Links to Get Images For Each
    for hemi in hemi_links:

        # Create a Dictionary For the Given Hemisphere
        hemi_dict = {}
        
        # Click Link with Corresponding Text
        browser.click_link_by_partial_text(hemi)
        
        # Pause to Load Webpage
        sleep(2)

        # Scrape Image URL and Store in Hemi_Dict
        hemi_dict['img_url'] = browser.find_by_text('Sample')['href']
        
        # Pull Title From Hemi_Links and Store in Hemi_Dict
        hemi_dict['title'] = hemi
        
        # Add Dictionary For Given Hemisphere to Hemi_Image_URLS
        hemi_image_urls.append(hemi_dict)
        
        # Navigate Back
        browser.back()

        # Pause to Load Webpage
        sleep(2)

    # Store Mars Hemispheres Image URLs in Scrape Results Dictionary
    mars_scrape_results['hemispheres'] = hemi_image_urls

    # Quit Browser After Scraping
    browser.quit()

    # Return results
    return mars_scrape_results