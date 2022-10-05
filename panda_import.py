import pandas as pd
import numpy as np
import re
from collections import Counter

data = pd.read_csv (r'C:\Users\pauli\Documents\naucse-python\pandatest\indeedEN.csv', nrows = 50) 
#read the csv file (put 'r' before the path string to address any special characters in the path, 
# such as '\'). Don't forget to put the file name at the end of the path + ".csv"

#df = pd.DataFrame(data, columns= ['company','id','description', 'location'])

data["DateOfScrape"]=data['scrapedAt'].str[:10]
data["DateOfScrape"] = pd.to_datetime(data["DateOfScrape"], format='%Y-%m-%d')
data["PostedPredDays"]= data['postedAt'].str.findall((r'\d+'))

# doprcic uz tohleto, proc to maze vsechno ? data["PostedPredDays"] = data["PostedPredDays"].str.replace("[\[,\]]",'', regex=True)

data["PostedPredDays"] = data["PostedPredDays"].str.join(',')
data["PostedPredDays"] = data["PostedPredDays"].str.strip()
#data["PostedPredDays"] = pd.to_numeric(data['PostedPredDays']) - potrebuju integer a nejde
#data["PostedPredDays"] = data["PostedPredDays"].astype(int) - integer nejde
data["OriginalDate"] = data["DateOfScrape"] - pd.to_timedelta(data['cislo'], unit='d')


data["EnglishDescr"]= data['description'].str.contains((' the '), regex=True, flags=re.IGNORECASE)
data["CzechDescr"]= data['description'].str.contains((r'^[Řř]\w*ř\w*'), regex=True, flags=re.IGNORECASE)

data["SQL"]= data['description'].str.contains('SQL', 'sql')
data["Python"]= data['description'].str.contains('Python', regex=True, flags=re.IGNORECASE)
data["Alteryx"]= data['description'].str.contains(('alteryx'), regex=True, flags=re.IGNORECASE)
data["Tableau"]= data['description'].str.contains(('tableau'), regex=True, flags=re.IGNORECASE)
data["PowerBI"]= data['description'].str.contains((r'Power BI | PowerBI'), regex=True, flags=re.IGNORECASE)
data["R"]= data['description'].str.contains((' R '), regex=True, flags=re.IGNORECASE)
data["Oracle"]= data['description'].str.contains(('Oracle'), regex=True, flags=re.IGNORECASE)
data["Snowflake"]= data['description'].str.contains(('Snowflake'), regex=True, flags=re.IGNORECASE)
data["MySQL"]= data['description'].str.contains((r' MySQL | My SQL'), regex=True, flags=re.IGNORECASE)
data["Postgre"]= data['description'].str.contains((r' postgre '), regex=True, flags=re.IGNORECASE)
data["Excel"]= data['description'].str.contains(('Excel'), regex=True, flags=re.IGNORECASE)
data[".NET"]= data['description'].str.contains(('.NET'), regex=True, flags=re.IGNORECASE)
data["Java"]= data['description'].str.contains(('Java'), regex=True, flags=re.IGNORECASE)

data["GermanLang"]= data[['description', 'positionName']].apply(lambda x: x.str.contains('German',case=False)).any(axis=1).astype(bool)
data["EnglishLang"]= data[['description', 'positionName']].apply(lambda x: x.str.contains((r'English| AJ '), regex=True, flags=re.IGNORECASE)).any(axis=1).astype(bool)
data["OtherLang"]= data[['description', 'positionName']].apply(lambda x: x.str.contains((r'Spanish|Portuguese|French|Greek|Chinese|Japanese|Russian|Norwegian|Swedish|Finnish|Danish|Dutch'), regex=True, flags=re.IGNORECASE)).any(axis=1).astype(bool)


data["Years"]= data['description'].str.extract((r'\s*(year|years|let|roků)'), flags=re.IGNORECASE)
data["Numbers"]= data['description'].str.findall((r'[0-9]+'))
data["NumYears"]= data['description'].str.findall((r'\d*\.?\d*\+?\s+(?:[Yy]ears|[Yy]ear|[Ll]et)|[Rr]oků'))

data["Junior"]= data['description'].str.contains(('junior'), regex=True, flags=re.IGNORECASE)
data["Medior"]= data['description'].str.contains((r'medior|intermediate|level 2'), flags=re.IGNORECASE)
data["Senior"]= data['description'].str.contains(r'senior', regex=True, flags=re.IGNORECASE)
data["Intern"]= data['description'].str.contains((r'intern|internship'), regex=True, flags=re.IGNORECASE)
data["PartTime"]= data['description'].str.contains((r'part-time|part time|parttime'), regex=True, flags=re.IGNORECASE)
data["FullTime"]= data['description'].str.contains((r'full-time|full time|fulltime'), regex=True, flags=re.IGNORECASE)
data["Maternity"]= data['description'].str.contains(r'maternity', regex=True, flags=re.IGNORECASE)
data["Remotely"]= data['description'].str.contains((r'remotely|remote|remote friendly'), regex=True, flags=re.IGNORECASE)
data["HomeOffice"]= data['description'].str.contains((r'home-office|home office|work from home|home-working|home working'), regex=True, flags=re.IGNORECASE)


#funguje na fulltext pocet opakovani
# filter_words = ['SQL', 'python', 'R']
# def add_words(x):
#     return ' '.join([
#         token 
#         for token in x.split(' ') 
#         if token in filter_words
#     ])
# data['words'] = data['description'].apply(lambda x: add_words(x))

    

data.to_csv('addedcolumn.csv', index = False)

