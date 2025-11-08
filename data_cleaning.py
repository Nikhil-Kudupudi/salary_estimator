# ###########################
# author: nikhil
#############################

import pandas as pd
import re
df= pd.read_csv("glassdoor_jobs.csv")

# salary parsing


df=df[df["Salary Estimate"] != '-1'] 
salary=df["Salary Estimate"].apply(lambda x: x.split("(")[0])
minus_Kd=salary.apply(lambda x: x.replace('K','').replace('$',''))

minhr=minus_Kd.apply(lambda x: x.lower().replace("per hour","").replace("employer provided",""))

df["min_salary"]=minhr.apply(lambda x: int(x.split('-')[0]))
df["max_salary"]=minhr.apply(lambda x: int(x.split('-')[1]))
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df["avg_salary"]=(df.min_salary+df.max_salary)/2
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided' in x.lower() else 0)

#company name text only
pattern = r'[^a-zA-Z\s]'
# remove any ratings from company name if there
df["Company Name"]=df["Company Name"].apply(lambda x:re.sub(pattern,"",x) )


# state field from location
df["state"]=df["Location"].apply(lambda x: x.split(",")[1] if "," in x else x)
print("state wide job counts", df["state"].value_counts())
df["same_State"]=df.apply(lambda x: 1 if x.Location==x.Headquarters else 0, axis=1)

# age of company from founded

df["age"]=df.Founded.apply(lambda x: x if x<1 else 2024 - x)
#parsing of job decription (python, etc)
# get skills matching from the job description
# python, java, c, c#, c++, ruby, javascript, spark, r studio, matlab, excel, aws, tableau, powerbi,gcp, sas , azure

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
#r studio 
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

#spark 
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

#aws 
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()


df.to_csv("salary_data_cleaned.csv",index=False)
