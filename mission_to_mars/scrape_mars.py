#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import datetime as dt
import time


def mars_news(browser):

    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
 
    html = browser.html
    soup = bs(html, "html.parser")


    try:
        news_element = soup.select_one('ul.item_list li.slide')
        news_element.find('div', class_='content_title')

        news_title = news_element.find('div', class_='content_title').text
        news_p = news_element.find('div', class_='article_teaser_body').text
    except AttributeError:
        return None, None
    return news_title, news_p


def featured_image(browser):
    feature_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(feature_image_url)
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.links.find_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = bs(html, "html.parser")   

    time.sleep(1)
    images = image_soup.select_one("figure.lede a img")
    try:
        images_url = images.get("src")
    except AttributeError:
        return None
    images_url = f"https://www.jpl.nasa.gov{images_url}"
    return images_url


def mars_facts():
    facts_url = 'https://space-facts.com/mars/'
    try:
        tables = pd.read_html(facts_url)[0]
    except BaseException:
        return None
    tables.columns=["Description", "Value"]
    tables.set_index("Description", inplace=True)
    return tables.to_html(classes="table table-striped")


def hemisphere(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    images_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": images_url,
        "mars_facts": facts,
        "hemispheres": hemisphere_image_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape())