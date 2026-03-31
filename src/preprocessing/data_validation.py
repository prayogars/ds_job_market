# %% Import important libraries
import pandas as pd
import numpy as np
import re

# %% Loading the data and checking the dataset
df = pd.read_csv("D:\\Data Science\\Project\\ds_job_market\\data\\cleaned_data.csv")
print(df.columns)
data = df.copy()
data = data.drop(columns=["min_salary", "max_salary", "avg_salary"])
print(f"Columns data type:\n{data.dtypes}\n")
print(f"Dataset info:\n{data.info()}")

# %% Fixing previous step so it produces more accurate results
def get_min_salary(text):
    
    if pd.isna(text) or str(text).lower() == "nan" or str(text).strip() == "":
        return np.nan
    numbers = re.findall(r"\d+", str(text))
    
    if not numbers:
        return np.nan
    return numbers[0]

data["min_salary"] = pd.to_numeric(
    data["salary_preCleaned"].apply(get_min_salary), 
    errors='coerce'
)

def get_max_salary(text):
    
    if pd.isna(text) or str(text).lower() == "nan" or str(text).strip() == "":
        return np.nan
    numbers = re.findall(r"\d+", str(text))
    
    if not numbers:
        return np.nan
    return numbers[-1]

data["max_salary"] = pd.to_numeric(
    data["salary_preCleaned"].apply(get_max_salary), 
    errors='coerce'
)

data["avg_salary"] = (data["min_salary"] + data["max_salary"]) / 2

# %% Dropping unimportant columns
data_formatted = data.drop(columns=["Unnamed: 0", "post_date", "job_description", "salary", "post_date_num", "scrape_date", "salary_preCleaned"])

print(f"Columns data type:\n{data_formatted.dtypes}\n")
print(f"Dataset info:\n{data_formatted.info()}")

# %% Converting columns data type
data_formatted["posted_at"] = pd.to_datetime(data_formatted["posted_at"])
data_formatted["posted_date_only"] = pd.to_datetime(data_formatted["posted_date_only"])

# %% Data validation
# Province Not Available because unvalid location and location not included at the preliminary list (58)
data_validated = data_formatted.copy()

for row in data_validated.itertuples():
    if row.province == "Not Available" and "yogyakarta" in str(row.location).lower():
        data_validated.at[row.Index, "province"] = "yogyakarta"
    elif row.province == "Not Available" and str(row.location).lower() == "indonesia":
        data_validated.at[row.Index, "province"] = "Not Available"
## extract rows with 'Not Available' province column
data_validated["location"] = data_validated.apply(lambda row: "Not Available" if row["province"] == "Not Available" and row["location"] != "Indonesia" else row["location"], axis=1)

# Remove posted_date_only column
data_validated = data_validated.drop(columns=["posted_date_only"])

#%% Saving the validated data
data_validated.to_csv("D:\\Data Science\\Project\\ds_job_market\\data\\validated_data.csv", sep="|", index=False, encoding="utf-8-sig")
