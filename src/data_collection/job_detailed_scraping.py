from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

PATH = "C:\\Program Files (x86)\\ChromeDriver\\chromedriver.exe" # Update this path to where your ChromeDriver is located

def scrape_job_details(job_links):
    service = Service(PATH)
    driver = webdriver.Chrome(service = service)
    job_title = []
    company_name = []
    location = []
    post_date = []
    job_description = []
    salary = []
    
    for link in job_links:
        driver.get(link)
        
        try:
            job_title_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[@data-automation = 'job-detail-title']"))
            )
            job_title.append(job_title_elem.text)
            
            company_name_elem = driver.find_element(By.XPATH, "//span[@data-automation='advertiser-name']")
            company_name.append(company_name_elem.text)
            
            location_elem = driver.find_element(By.XPATH, "//a[@tabindex = '-1']")
            location.append(location_elem.text)
            
            posting_date_elem = driver.find_element(By.XPATH, "//*[contains(text(), 'Posted')]")
            post_date.append(posting_date_elem.text)
            
            try:
                salary_elem = driver.find_element(By.XPATH, "//span[@data-automation = 'job-detail-salary']")
                salary.append(salary_elem.text)
            except NoSuchElementException:
                salary.append("Not Available")
                        
            job_description_elem = driver.find_element(By.XPATH, "//div[@data-automation = 'jobAdDetails']")
            job_description.append(job_description_elem.text)
            
            print(f"Scraped details for {link} with job title: {job_title_elem.text} and company: {company_name_elem.text} at location: {location_elem.text} {posting_date_elem.text} with job description length: {len(job_description_elem.text)}")
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"  Error scraping {link}: {e}")

    time.sleep(5)
    driver.quit()
    return job_title, company_name, location, post_date, job_description, salary

def save_job_details_to_csv(job_title, company_name, location, post_date, job_description, salary):
    job_details_df = pd.DataFrame({
        "job_title": job_title,
        "company_name": company_name,
        "location": location,
        "post_date": post_date,
        "job_description": job_description,
        "salary": salary
    })
    
    job_details_df.to_csv("D:\\Data Science\\Project\\ds_job_market\\data\\job_details_indonesia.csv")
    
# job_title, job_post_link_id, company_name, location, post_date, job_description = scrape_job_details(job_links)

# print(f"Scraped {len(job_title)} job details successfully.")

# save_job_details_to_csv(job_title, job_post_link_id, company_name, location, post_date, job_description)
