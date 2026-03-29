# Starting with Selenium WebDriver to scrape data from JobStreet
# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe" # Update this path to where your ChromeDriver is located
service = Service(PATH) 
driver = webdriver.Chrome(service=service)
# Cookies : o9RmkDy9hXxooBlZJoN5iS4uQsmAzhktVbcxKQalmAIAANCl4tlOQwFi4QAAADxm4ZwXIJaBSwAAALwkxYOqKaGkEgAAAB71NcqXBrlQBgAAAA (DV)
# Setting up the Chrome WebDriver

# Function for scraping per country
def scrape_job_links(keywords, domain, country_label):
    """
    Parameters:
    
    keywords: Job title that you want to find
    domain: Website domain
    country_label: country that you're searching in
    
    Return:
    List of all job posting links according to the parameters
    """
    all_hrefs = []
    for keyword in keywords:
        search_keyword = keyword.replace(" ", "-")
        search_url = f"https://{domain}/en/job-search/{search_keyword}-jobs/"
        print(f"\nSearching on {country_label.upper()} for: {keyword.upper()} jobs")
        driver.get(search_url)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-automation='normalJob']"))
            )
            job_links_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-automation = 'job-list-view-job-link']")
            hrefs = [el.get_attribute("href") for el in job_links_elements if el.get_attribute("href")]
            all_hrefs.extend(hrefs)
            
            print(f"  Found {len(hrefs)} job links in {country_label} for '{keyword}' in  page 1")
            
            for i in range(2, 15):
                try:
                    driver.find_element(By.XPATH, f"//a[@data-automation = 'page-{i}']").click()
                
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-automation = 'jobTitle']"))
                    )
                    
                    job_links_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-automation = 'job-list-view-job-link']")
                    hrefs_pages = [el.get_attribute("href") for el in job_links_elements if el.get_attribute("href")]
                    all_hrefs.extend(hrefs_pages)
                    
                    print(f"Found {len(hrefs_pages)} job links in {country_label} for '{keyword}' in  page {i}")
                    time.sleep(2)  # Sleep to avoid overwhelming the server
                except:
                    print(f"  No more pages found for: {keyword} in {country_label} after page {i-1}")
                    break
                
        except TimeoutException:
            print(f"  Timeout loading results for: {keyword} in {country_label}")
            
        except NoSuchElementException:
            print(f"No element found for: {keyword} in {country_label}")
    return all_hrefs

# link_df = pd.DataFrame(all_job_hrefs_indonesia, columns=["href", "country"])
# link_df.to_csv("jobstreet_job_links_indonesia.csv", index=True)
# print(f"\nTotal job links scraped for Indonesia: {len(all_job_hrefs_indonesia)}")