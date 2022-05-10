# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    print("scraping.py line 14")
    
    # Run all scraping functions and store results in a dictionary
    #In the def scrape_all() function in your scraping.py file, create a new dictionary in the data dictionary to hold a list of dictionaries with the URL string and title of each hemisphere image.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        #"last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_scrape(browser)
    }
    print(data)
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    print("scraping.py", 44)
    # Add try/except for error handling
    try:
        print("scrapng.py", 47)
        slide_elem = news_soup.select_one('div.list_text')
        print("scrapng.py", 49)
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        print("scrapng.py", 52)
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        print("scrapng.py", 55)

    except AttributeError:
        return None, None

    return news_title, news_p



def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url



def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://galaxyfacts-mars.com/')[0]
        print("99", df)

    except BaseException as err:
        print(err)
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()



def hemisphere_scrape(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # 1. Use browser to visit the URL 
    url2 = 'https://marshemispheres.com/'
    browser.visit(url2)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []


    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html


    # Retrieve the parent divs for all images
    parent_divs = browser.find_by_css('div.description a.product-item')
    #parent_divs = img_soup.find_all('div', class_='item')
    print(len(parent_divs))

    for item in range(len(parent_divs)):
        #Scrape title
        browser.find_by_css('div.description a.product-item')[item].click()  
        img_url_title = browser.find_by_tag('h2').text
        
    #Scrape image URL
    #Add try/except for error handling
        try:
            img_url_rel = browser.find_by_css('div.downloads a').first['href']
        
        except AttributeError:
        #return None, or print exception
            print(f"There was an exception")

    # Use the base url to create an absolute url
        img_url = f'https://marshemisphere.com/{img_url_rel}'
    

    # Run all scraping functions and store results in a dictionary
        hemispheres = {
            "img_url": f'{img_url_rel}',
            "title": img_url_title
        }
    
        hemisphere_image_urls.append(hemispheres)
    
        browser.back()
        
    return hemisphere_image_urls
    



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


    