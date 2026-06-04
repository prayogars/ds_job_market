# 📊 Data Job Market in Indonesia

An end-to-end data project that scrapes, cleans, and visualizes job postings for data roles in Indonesia — helping job seekers and organizations understand the current data job landscape.

---

## 🎯 Background

There is limited publicly available insight about the data job market in Indonesia, including demand trends, salary ranges, required skills, and geographic distribution. This project aims to bridge that gap by collecting real-world job postings and turning them into actionable insights.

**Target Users:**
- Job seekers pursuing data science, analytics, or engineering careers
- Job market platforms wanting to provide insights about the data science job market

---

## ❓ Business Questions

1. What is the current demand for data roles in Indonesia?
2. What skills are most required for data roles?
3. Which locations have the highest demand?
4. How has demand changed over time?
5. What is the typical salary range for data roles in Indonesia?

---

## 📁 Project Structure

```
ds_job_market/
├── data/
│   └── job_details_indonesia.csv     # Raw scraped data
├── job_links_scraping.py             # Scrapes job listing URLs from Jobstreet
├── job_detailed_scraping.py          # Scrapes detailed info per job listing
├── main.py                           # Entry point: runs the full scraping pipeline
├── data_cleaning.py                  # Cleans and transforms raw data
└── cleaned_data.csv                  # Final cleaned dataset
```

---

## 🔄 Pipeline Overview

### 1. Scraping (`main.py`)
Scrapes job listings from **id.jobstreet.com** for three keywords:
- `data scientist`
- `data analyst`
- `data engineer`

Collects: job title, company name, location, post date, job description, and salary.

### 2. Data Cleaning (`data_cleaning.py`)
- Removes duplicate listings
- Extracts **province** from location strings using Indonesian province name matching
- Converts relative post dates (e.g., `2d`, `3h`, `1mo`) into actual timestamps
- Filters to data-related job titles
- Detects skill mentions in job descriptions (SQL, Python, Tableau, Power BI, AWS, Spark, etc.)
- Parses salary ranges into `min_salary`, `max_salary`, and `avg_salary` columns

### 3. Visualization (Tableau)
An interactive dashboard showing:
- Total job postings & companies
- Job postings by province (map)
- Job postings trend over time
- Salary distribution
- Skills frequency ranking
- Experience requirement breakdown

---

## 📈 Key Metrics

| Metric | Value |
|---|---|
| Total Job Postings | 202 |
| Unique Companies | 174 |
| Data Scraped | March 18, 2026 |
| Source | id.jobstreet.com |

---

## 🛠️ Skills Tracked

`SQL` · `Python`· `Tableau` · `PostgreSQL` · `GitHub` · `BeautifulSoup` · `Selenium`

---

## ⚙️ How to Run

**1. Install dependencies**
```bash
pip install pandas numpy requests beautifulsoup4
```

**2. Run the scraper**
```bash
python main.py
```

This will scrape job links and details from Jobstreet and save the results to `data/job_details_indonesia.csv`.

**3. Run data cleaning**
```bash
python data_cleaning.py
```

Output: `cleaned_data.csv` — ready for analysis or Tableau import.

---

## 📊 Dashboard Preview

![Data Job Market in Indonesia Dashboard]([Dashboard_1.png](https://public.tableau.com/views/ds_job_market_dashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link))

---

## 📌 Notes

- Job postings older than 30 days (`30d+`) are excluded from the analysis.
- Salary data is only available for a subset of listings; many postings do not disclose salary.
- Province extraction is based on keyword matching against all 38 Indonesian provinces.
