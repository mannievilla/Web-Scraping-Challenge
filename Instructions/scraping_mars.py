

from this import d
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    data = {}

    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news = soup.select_one("div.list_text")

    news_title = news.find("div", class_="content_title").get_text()

    news_p = news.find("div", class_="article_teaser_body").get_text()

    data["news_title"] = news_title
    data["news_paragraph"] = news_p

    url = "https://spaceimages-mars.com"
    browser.visit(url)

    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img_url_rel = soup.find('img', class_='fancybox-image')
  
    img_url_rel = soup.find('img', class_='fancybox-image').get('src')

    img_url ="https://spaceimages-mars.com/" + img_url_rel

    data["featured_image"] = img_url

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.head()

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    df.to_html()

    data["facts"] = df.to_html()

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    import time 

    browser.is_element_present_by_text("USGS Astrogeology Science Center", wait_time=1)
    hemisphere_image_urls = []
    for i in range(4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(1)
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
    #     html = browser.html
    #     hemi_soup = soup(html, "html.parser")
    #     hemisphere['img_url'] = hemi_soup.find("a", text="Sample").get("href")
    #     hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()
    #     hemisphere_image_urls.append(hemisphere)
        browser.back()
    hemisphere_image_urls

    data["hemispheres"] = hemisphere_image_urls

    browser.quit()

    return data



