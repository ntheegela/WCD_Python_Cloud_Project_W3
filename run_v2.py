#!/usr/bin python3
"""
This is the main file for the py_cloud project. It can be used at any situation
"""
import requests
import json
import pandas as pd
def company_to_csv_date():
    url = "https://www.themuse.com/api/public/jobs?page=50"
    req = requests.get(url)
    content = req.json()
    company_list=[]
    publication_list=[]
    job_list=[]
    job_type_list=[]
    location_list=[]
    for i in content['results']:
        company =i['company']['name']
        company_list.append(company)
        company_name={'Company':company_list}
        publication_date=i['publication_date'] 
        publication_list.append(publication_date)
        pulished_date={'Published':publication_list}
        job_name=i['name']
        job_list.append(job_name)
        job={'Job':job_list}
        job_type=i['type']
        job_type_list.append(job_type)
        typeof_job={'Job_Type':job_type_list}
        for loc_name in i['locations']:
            location=loc_name['name']
            location_list.append(location)
            location_name={'Location':location_list}
    df_comp=pd.DataFrame(company_name)
    df_location=pd.DataFrame(location_name)
    df_job=pd.DataFrame(job)
    df_jobtype=pd.DataFrame(typeof_job)
    df_publ=pd.DataFrame(pulished_date)
    df_final=pd.concat([df_comp,df_location,df_job,df_jobtype,df_publ],axis=1)
    df_final[['City','Country']]=df_final['Location'].astype(str).str.split(',',expand=True)
    df_final['Published']=pd.to_datetime(df_final['Published']).dt.tz_localize(None).dt.strftime('%Y-%m-%d')
    df_final.drop('Location', axis=1, inplace=True)
    df_final = df_final.reindex(columns=['Company','Country','City','Job','Job_Type','Published'])
    df_final.to_csv('jobs.csv',index=False)
company_to_csv_date()        
print('dataframe saved to local')

# use linux command to upload file to S3
subprocess.run(['aws', 's3', 'cp', 'jobs.csv', 's3://wcd-week3-python-project/csv_files/jobs.csv'])
# Success.
print('File uploading Done!')





    


    
