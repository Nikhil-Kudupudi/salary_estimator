import glassdoor_scraper as gs

path="D:/gitRepos/salary_estimator/chromedriver"

df=gs.get_jobs("data scientist",15,True,path)
df.to_csv("glassdoor_jobs.csv",index=False)