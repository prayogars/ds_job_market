from job_links_scraping import scrape_job_links
from job_detailed_scraping import scrape_job_details, save_job_details_to_csv

job_links = scrape_job_links(keywords=["data scientist", "data analyst", "data engineer"], domain="id.jobstreet.com", country_label="Indonesia")

job_title, company_name, location, post_date, job_description, salary = scrape_job_details(job_links)

save_job_details_to_csv(job_title, company_name, location, post_date, job_description, salary)



