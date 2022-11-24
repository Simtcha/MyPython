import pandas as pd
import os
import glob
import numpy as np
import re
from textblob import TextBlob
from langdetect import detect



data = pd.read_csv (r'C:\Users\pauli\Documents\naucse-python\DA\MeGity\out.c-spojeni-indeed-pokus-2.temp_4.csv', encoding ='utf-8',nrows = 50000) 

# mazat duplikaty
data.drop_duplicates(subset="id", inplace=True)
# VSECHNO LOWERCASE#
data = data.applymap(lambda s: s.lower() if type(s) == str else s)

data["DateOfScrape"]=data['scrapedAt'].str[:10] # extrahuje datum ze sloupce 'scrapedAt' a ulozi do sloupce 'DateOfScrape'
data["DateOfScrape"] = pd.to_datetime(data["DateOfScrape"], format='%Y-%m-%d') # predela extrahovane datum na datovy typ date

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# funguje ok
data["PostedPredDays"] = data.apply(lambda x: 0 if has_numbers(x["postedAt"])==False else int(x["postedAt"][-6:-4].replace(" ","")), axis=1)
data["OriginalDate"] = data["DateOfScrape"] - pd.to_timedelta(data['PostedPredDays'], unit='d')

# jazyk inzeratu - funguje ok
data["detected_description_language"] = data.apply(lambda x: detect(x["description"]), axis=1)
data["pocet_ang_slov_v_description"] = data.apply(lambda a: sum(a["description"].count(x) for x in ("the", "of", "we are", "for", "with")), axis=1)
data["pocet_ceskych_znaku_v_description"] = data.apply(lambda a: sum(a["description"].count(x) for x in ("ř", "š", "č", "ž", "ě", "ý", "á", "í", "é", "ú", "ů")), axis=1)
data["detected_description_language_final"] = data.apply(lambda x: "en" if (x["detected_description_language"]=="cs")&\
                                                         (x["pocet_ang_slov_v_description"]>20)&\
                                                         (x["pocet_ceskych_znaku_v_description"]<200) else x["detected_description_language"], axis=1)

# skill detection
data["SQL"]= data['description'].str.contains((r'sql+[^a-z]|sql+[^a-z]|SQLkem'), regex=True, flags=re.IGNORECASE)
data["Python"]= data['description'].str.contains((r'Python'), regex=True, flags=re.IGNORECASE)
data["Spark"]= data['description'].str.contains((r' spark+[^a-z]|[^a-z]spark'), regex=True, flags=re.IGNORECASE)
data["C#"]= data['description'].str.contains((r'C#'), regex=True, flags=re.IGNORECASE)
data["Java"]= data['description'].str.contains((r'Java+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["Scala"]= data['description'].str.contains((r'Scala+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["Alteryx"]= data['description'].str.contains((r'alteryx+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["Tableau"]= data['description'].str.contains((r'tableau+[^a-z]|tablo+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["PowerBI"]= data['description'].str.contains((r'Power BI+[^a-z]|PowerBI+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["Qlik"]= data['description'].str.contains((r'Qlik+[^a-z]|Qlik+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["R"]= data['description'].str.contains((r'R-ko | Rkem | R-kem |\br+\s|\(r\b|\br\)|\br\/'), regex=True, flags=re.IGNORECASE)
data["Oracle"]= data['description'].str.contains((r'oracle+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["Snowflake"]= data['description'].str.contains((r'Snowflake+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["MySQL"]= data['description'].str.contains((r' MySQL+[^a-z]|My SQL+[^a-z]|mssql|ms-sql'), regex=True, flags=re.IGNORECASE)
data["Postgres"]= data['description'].str.contains((r'postgre+[^a-z]|postgres+[^a-z]|postgresql+[^a-z]|possgrest'), regex=True, flags=re.IGNORECASE)
data["Excel"]= data['description'].str.contains((r'excel+[^a-z]|excelov[ý,ým]|xls'), regex=True, flags=re.IGNORECASE) # excellence to nebere uz tak jak to je, bere to i Excel, Excel; atd
data[".NET"]= data['description'].str.contains((r'[^a-z]\.NET'), regex=True, flags=re.IGNORECASE)
data["Java"]= data['description'].str.contains((r'java+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["UML"]= data['description'].str.contains((r'UML+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["Enterprise Architect"]= data['description'].str.contains((r'\benterprise architect\b'), regex=True, flags=re.IGNORECASE)
data["Cognos"]= data['description'].str.contains((r'cognos+[^a-z]'), regex=True, flags=re.IGNORECASE)
data["GIT"]= data['description'].str.contains((r'\bGIT\b|\bgitlab\b|\bgithub\b'), regex=True, flags=re.IGNORECASE)
data["JIRA/Confluence"]= data['description'].str.contains((r'\bjira\b|\bconfluence\b|\batlassian\b'), regex=True, flags=re.IGNORECASE)
data["AWS"]= data['description'].str.contains((r'\bAWS\b|\bAmazon Web Services\b|\bAmazon Web\b'), regex=True, flags=re.IGNORECASE)
data["Azure"]= data['description'].str.contains((r'azure'), regex=True, flags=re.IGNORECASE)
data["TestingFlag"]= data['description'].str.contains((r'testing'), regex=True, flags=re.IGNORECASE)
data["CyberSecurityFlag"]= data['description'].str.contains((r'cyber security|cybersecurity|kybernetick[á,é,ý]+ bezpečnost+[ní,í,i]?'), regex=True, flags=re.IGNORECASE)
data["CommonSense"] = data['description'].str.contains((r'selský rozum|common sense|(analytical(\s+|\w+){0,4}\s+(skills|abilities))|logical thinking|logické myšlení|analytické myšlení|(analytical (mindset|thinking))'), regex=True, flags=re.IGNORECASE)
data["DataAnalysis"] = data['description'].str.contains((r'analýza dat|datová analýza|(analyzovat(\s|\w+){0,2}\s+data)|(analyzováním(\s+|\w+){0,2}\s+dat)|data analysis|datových analytiků|datové analýzy|datová analytika|analytika dat|datovou analytiku|datové analytiky|data analyst'), regex=True, flags=re.IGNORECASE)
data["Fruit"] = data['description'].str.contains((r'\bfruit[s]?\b|fruits+[^a-z]|\bovoc'), regex=True, flags=re.IGNORECASE)

# language wanted detection - funguje ok - tady je potřeba dodělat české verze other jazyků
regexp_nemcina = re.compile(r'(něm((čin)|(eck)))|(german[^y])')
data["german_lang_wanted"] = data.apply(lambda x: True if (x["detected_description_language"]=="de")|\
                                        (bool(regexp_nemcina.search((x['description']).lower()))) else False, axis=1)
regexp_anglictina = re.compile(r'(angli((čtin)|(ck)))|english')
data["english_lang_wanted"] = data.apply(lambda x: True if (x["detected_description_language"]=="en")|\
                                        (bool(regexp_anglictina.search((x['description']).lower()))) else False, axis=1)
regexp_other_lang = re.compile(r'spanish|španělský jaz|španělšti|španělsky|portuguese|portugalšti|portugalsky|portugalský jaz|french|francouzšti|francouzsky|francouzský jaz|greek|řečtin|řecky|řecký jaz|chinese|čínštin|čínsky|čínský jaz|japanese|japonš|japonsky|japonský jaz|russian|ruštin|rusky|ruský jaz|norwegian|noršti|norsky|norský jaz|swedish|švédšt|švédsky|švédský jaz|finnish|finšti|finsky|finský jaz|danish|dánšti|dánsky|dánský jaz|dutch|holandšt|holandský jaz|holandsky|other language|EU language|evropského jazyk|evropský jazyk')
data["other_than_cz_lang_wanted"] = data.apply(lambda x: (bool(regexp_other_lang.search((x['description']).lower())))|(x["detected_description_language"] not in ["cs", "en", "de"]), axis=1)

#pracovni podminky

def junior_medior_senior(nazev_pozice, popis_pozice):
    slovnik_levelu = {"senior": ["senior", "teamlead", "team lead", "team-lead", "vedoucí datových", "medior"],
                     "junior": ["junior", "juniory"]}
    level_final = "N/A"
    for level,level_label in slovnik_levelu.items():
        for label in level_label:
            if label in nazev_pozice:
                level_final = level
    if level_final =="N/A":
        for level,level_label in slovnik_levelu.items():
            for label in level_label:
                if label in popis_pozice:
                    level_final = level
    return level_final

list_sloupec_junior_senior_medior = []
for i in range(len(data)):
    nazev_pozice = data.iloc[i]["positionName"]
    popis_pozice = data.iloc[i]["description"]
    list_sloupec_junior_senior_medior.append(junior_medior_senior(nazev_pozice, popis_pozice))
data['junior_senior'] = list_sloupec_junior_senior_medior


data["StartingPosition"]= data[['description', 'positionName']].apply(lambda x: x.str.contains((r'intern+[^a-z]|internship|student/ka|pro absolv[a-z]*|pro student[a-z]*'),regex=True, flags=re.IGNORECASE)).any(axis=1).astype(bool)
data["PartTime"]= data[['description', 'positionName']].apply(lambda x: x.str.contains((r'part-time|part time|parttime|částečný úvazek|úvazek částečný|zkrácený|\bDPP\b|\bDPČ\b'),regex=True, flags=re.IGNORECASE)).any(axis=1).astype(bool)
data["FullTime"]= data[['description', 'positionName']].apply(lambda x: x.str.contains((r'full-time|full time|fulltime|plný úvazek|úvazek plný|\bHPP\b'),regex=True, flags=re.IGNORECASE)).any(axis=1).astype(bool)
data["HomeOffice/Remote"]= data[['description','positionName', 'location']].apply(lambda x: x.str.contains((r'home-office|home office|work from home|home-working|home working|remotely|remote+[^a-z]|remote friendly|práce na dálku|práce z domova|z domu|vzdálená práce|cafeoffice|Práce je možná z domova'), regex=True, flags=re.IGNORECASE)).any(axis=1).astype(bool)
data["PositionKeyWords"] = data['positionName'].str.findall((r'data|analyst|datov[ý,á]|analyti[a-z,č]|analýza|[Dd]ata [Ss]cientist'), flags=re.IGNORECASE)
data["PositionArea"] = data['positionName'].str.findall((r'HR|Finance|Financial|finan+[c,č]|Accounting|Pricing|nákladov|nákup|Inventory|Supply Chain|Salesforce|Sales|Purchase|Revenue|Marketing|Market|Change|PMO|Cloud|\bIT\b|Developer|vývoj[a-z]|\S?\s?DWH|Security|Web|Report|Reporting|ERP|Support|Engineering|SAP|Expense|Test|Sourcing|Softw|Software Development|\
Business|Archit|Product|Application|aplikač|\bBI\b|Compliance|Risk|Media|Testing|tester|Services|Systems|System|Systém[a-z]|Service Desk|Realtime|Technical|Logistics|Data Governance|Engineer|inžen|Scrum|Master Data|Data Protection|Real Estate|Arch|Pharma|Operations'), flags=re.IGNORECASE)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def find_all_numbers(text):
    list_pozic_cisel = []
    for i in range(0, 10):
        list_pozic_cisel.append(list(find_all(text, str(i))))
    narovnany_list = [item for sublist in list_pozic_cisel for item in sublist]
    return narovnany_list

def roky_zkusenosti(text):
    slova_zkusenosti = ["zkušenost", "zkusenost", "praxe", "experience"]
    list_textiku_nenarovnany = []
    for slovo in slova_zkusenosti:
        list_textiku_nenarovnany.append(list(find_all(text.lower(), slovo)))
    kde_je_experience = [item for sublist in list_textiku_nenarovnany for item in sublist]
    list_textiku = []
    list_roku = []
    for zacatek in kde_je_experience:
        if (zacatek-40)<0:
            start = 0
        else:
            start = zacatek-40
        end = zacatek+40
        textik = text[start:end]
        textik = textik.replace("-", " ")
        if "cyber operations with over 8 years of experience with cyber security" in textik:
            textik = "nic"
        list_roku_v_ruznych_jazycich = ["rok", "roků", "roku", "let", "year", "years"]
        if any(slovo_rok in textik for slovo_rok in list_roku_v_ruznych_jazycich):
            if any(char.isdigit() for char in textik):
                list_textiku.append(textik)
                roky = re.findall(r'\d+', textik)
                list_roku.append(roky)
    narovnany_list_roku = [item for sublist in list_roku for item in sublist]
    try:
        minimalni_roky_zkusenosti = min([eval(i) for i in narovnany_list_roku])
    except ValueError:
        minimalni_roky_zkusenosti = None
    if minimalni_roky_zkusenosti==None:
        minimalni_roky_zkusenosti = None
    elif minimalni_roky_zkusenosti>10:
        minimalni_roky_zkusenosti=None
    elif minimalni_roky_zkusenosti==0:
        minimalni_roky_zkusenosti=None
    return minimalni_roky_zkusenosti

list_sloupec_roky_zkusenosti = []
for i in range(len(data)):
    textik = data.iloc[i]["description"]
    list_sloupec_roky_zkusenosti.append(roky_zkusenosti(textik))

data['years_of_experience'] = list_sloupec_roky_zkusenosti

#vytvoreni noveho excelu s pridanymi sloupci
data.to_csv('final34.csv', index = False)
