import pandas as pd
import numpy as np

SCRAPE_DATE = "2026-03-18 01:00:00"
df = pd.read_csv("D:\\Data Science\\Project\\ds_job_market\\data\\job_details_indonesia.csv")
print(df.describe())

raw_data = df.copy()

pd.set_option("display.min_rows", None)
pd.set_option("display.max_rows", None)

# handling duplicate
print(raw_data.head())
raw_data.duplicated(subset = ["job_title", "company_name", "location", "post_date"]).value_counts()
raw_data = raw_data.drop_duplicates(subset=["job_title", "company_name", "location", "post_date"], keep="first")

# job province
indo_provinces = [
    "aceh",
    "north sumatra",
    "west sumatra",
    "riau",
    "riau islands",
    "jambi",
    "south sumatra",
    "bengkulu",
    "lampung",
    "bangka belitung islands",
    "jakarta",
    "west java",
    "central java",
    "special region of yogyakarta",
    "east java",
    "banten",
    "bali",
    "west nusa tenggara",
    "east nusa tenggara",
    "west kalimantan",
    "central kalimantan",
    "south kalimantan",
    "east kalimantan",
    "north kalimantan",
    "north sulawesi",
    "central sulawesi",
    "south sulawesi",
    "southeast sulawesi",
    "gorontalo",
    "west sulawesi",
    "maluku",
    "north maluku",
    "west papua",
    "papua",
    "south papua",
    "central papua",
    "highland papua",
    "southwest papua"
]
indo_provinces = '(' + '|'.join(indo_provinces) + ')'

raw_data["province"] = raw_data["location"].str.lower().str.extract(indo_provinces, expand=False).fillna("Not Available")

# post date
## date and time the data scraped: 18/3/2026 at 1 AM
raw_data["post_date_num"] = raw_data["post_date"].apply(lambda x: x.split(" ")[1])
raw_data["scrape_date"] = pd.to_datetime(SCRAPE_DATE)

print(raw_data[raw_data["post_date_num"].str.strip() == "30d+"])
print(raw_data["post_date_num"][raw_data["post_date_num"].str.strip() == "30d+"].value_counts())
raw_data = raw_data[raw_data["post_date_num"].str.strip() != "30d+"]
    
def convert_to_timedelta(text):
    text = str(text).lower()
    
    if "d" in text:
        days = text.replace("d", "")
        return pd.to_timedelta(int(days), unit="D")
    elif "h" in text:
        hours = text.replace("h", "")
        return pd.to_timedelta(int(hours), unit="h")
    elif "mo" in text:
        month = text.replace("mo", "")
        days = int(month) * 30
        return pd.to_timedelta(days, unit="D")
    else:
        return pd.to_timedelta(0)

time_offset = raw_data["post_date_num"].apply(convert_to_timedelta)

raw_data["posted_at"] = raw_data["scrape_date"] - time_offset

raw_data["posted_date_only"] = raw_data["posted_at"].dt.date

# job desc: sql, python, spark, AI, ML
filter_data = raw_data[raw_data["job_title"].str.lower().str.contains("data|analyst", na=False)]
print(filter_data["job_title"].value_counts())
print(filter_data.columns)

skills_to_check = ["python", "sql", "mysql", "postgresql", "database", "aws", "azure", "spark", "hadoop", "kafka", "snowflake", "databricks", "apache", "git", "github", "tableau", "power bi", "looker"]

for skill in skills_to_check:
    column_name = f"{skill}_yn"
    filter_data[column_name] = filter_data["job_description"].str.lower().str.contains(skill, na=False).astype(int)

# experience
## bachelor's, years, tahun
experience_to_check = ["years", "bachelor's", "tahun"]
for experience_needed in experience_to_check:
    filter_data["experience_needed_yn"] = filter_data["job_description"].str.lower().str.contains(experience_needed, na=False).astype(int)
    
# salary parsing
filter_data["salary_preCleaned"] = (
    filter_data["salary"]
    .str.replace("Rp", "", regex=False)
    .str.replace("per month", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
filter_data["salary_preCleaned"] = filter_data["salary_preCleaned"].replace("Not Available", np.nan)

temp_salary = filter_data["salary_preCleaned"].str.replace(".", "", regex=False)
filter_data["min_salary"] = pd.to_numeric(temp_salary.str.split("-").str[0], errors='coerce')
filter_data["max_salary"] = pd.to_numeric(temp_salary.str.split("-").str[1], errors='coerce')
filter_data["max_salary"] = filter_data["max_salary"].fillna(filter_data["min_salary"])
filter_data["avg_salary"] = (filter_data["min_salary"] + filter_data["max_salary"]) / 2

print(filter_data[["salary", "min_salary", "max_salary", "avg_salary"]].head())

filter_data.to_csv("cleaned_data.csv", index=False)
