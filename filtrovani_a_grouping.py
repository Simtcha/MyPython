import pandas as pd



data = pd.read_csv(r'C:\Users\pauli\Documents\naucse-python\DA\MeGity\final34.csv', encoding ='utf-8') 

data = data[~((data.DataAnalysis == False) & (data.PositionKeyWords.str.len()==2) & (data.PositionArea.str.len()==2) & (data.SQL == False))]
data = data[~(data.positionName.str.contains(r'payable|purchase|service desk analyst|actuar[yi]|ux|\baccounting\b|\bpayroll\b|\baudit\b|\bkyc\b|\bcollections\b|\bjava engineer\b|\bjava deverlopper\b|\bap analyst\b|\baccounts payable\b|\bprocurement\b|\bscrum\b|\bsoftware engineer\b|\bkotlin\b'))]
data.drop(['externalApplyLink','description', 'url', 'pocet_ang_slov_v_description', 'pocet_ceskych_znaku_v_description', 'reviewsCount', 'rating'], axis=1, inplace = True)

data.to_csv('final331.csv', index = False)

#vytvoreni noveho csv jako overview
data = pd.read_csv(r'C:\Users\pauli\Documents\naucse-python\DA\MeGity\final331.csv', encoding ='utf-8') 

listy = ['SQL', 'Python', 'Spark', 'C#','Java', 'Scala', 'Alteryx', 'Tableau', 'PowerBI', 'Qlik', 'R', 'Oracle', 'Snowflake', 'MySQL', 'Postgres', 'Excel', '.NET', 'UML',
       'Enterprise Architect', 'Cognos', 'GIT', 'JIRA/Confluence', 'AWS', 'Azure', 'TestingFlag', 'CyberSecurityFlag', 'CommonSense', 'DataAnalysis', 'Fruit', 'german_lang_wanted', 'english_lang_wanted',
       'other_than_cz_lang_wanted', 'StartingPosition', 'PartTime', 'HomeOffice/Remote']

slovnik = {}

for i in listy:
       slovnik[i] = data[i].sum()

df3 = data.groupby(['junior_senior']).size().reset_index(name='Count')
df3.rename(columns = {'junior_senior':'Skill'}, inplace = True)
novy = pd.DataFrame(slovnik.items(), columns=['Skill', 'Count'])
novy = pd.concat([novy, df3],axis = 0, join = 'outer', ignore_index=True)
todelete2 = novy[(novy.Skill.str.contains(r'N/A'))].index
novy.drop(todelete2 , inplace=True)

novy.to_csv('overview.csv', index = False)
