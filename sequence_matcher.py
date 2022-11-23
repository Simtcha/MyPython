from difflib import SequenceMatcher
import pandas as pd

# df_pd_cetnost_linky_api_title = pd.read_csv (r'C:\Users\pauli\Documents\naucse-python\pandatest\dataset_indeed-scraper_2022-10-04_05-34-16-657(mod).csv', encoding ='utf-8',nrows = 500) 

delka_df_pd_cetnost_linky_api_title = len(df_pd_cetnost_linky_api_title.index)
results_match_str = []
results_match_len = []
results = []
for radek in range(delka_df_pd_cetnost_linky_api_title):
    try:
        query = df_pd_cetnost_linky_api_title.iloc[radek,0]
        title = df_pd_cetnost_linky_api_title.iloc[radek,6]
        # odstranit z query tecky
        query_bez_pomlcky = query.replace("-", " ")
        query_bez_zavorek_prednich = query_bez_pomlcky.replace("(", "")
        query_bez_zavorek_zadnich = query_bez_zavorek_prednich.replace(")", "")
        query_bez_plus = query_bez_zavorek_zadnich.replace("+", " ")
        query_bez_carky = query_bez_plus.replace(",", " ")
        query_bez_dvojtecky = query_bez_carky.replace(":", " ")
        query_bez_tecky = query_bez_dvojtecky.replace(".", " ")
        # odstranit z titulku pomlcky a zavorky
        title_bez_pomlcky = title.replace("-", " ")
        title_bez_zavorek_prednich = title_bez_pomlcky.replace("(", "")
        title_bez_zavorek_zadnich = title_bez_zavorek_prednich.replace(")", "")
        title_bez_plus = title_bez_zavorek_zadnich.replace("+", " ")
        title_bez_carky = title_bez_plus.replace(",", " ")
        title_bez_dvojtecky = title_bez_carky.replace(":", " ")
        title_bez_tecky = title_bez_dvojtecky.replace(".", " ")
        # z obojiho udelat listy a ty porovnat
        list_query = query_bez_tecky.split(" ")
        list_title = title_bez_tecky.split(" ")
        spolecne = list(set(list_query).intersection(list_title))
        if query==title:
                typ_shody = "presna_shoda"
        elif len(spolecne)>0:
            typ_shody = "castecna_shoda"
        else:
            typ_shody = "zadna_shoda"
        # nejdelsi spolecny retezec
        match = SequenceMatcher(None, query_bez_tecky, title_bez_tecky).find_longest_match(0, len(query_bez_tecky), 0, len(title_bez_tecky))
        match_str = query_bez_tecky[match.a: match.a + match.size]
        match_len = len(match_str)
    except:
        match_str = "organicky_titulek_neni_zalogovan"
        match_len = "organicky_titulek_neni_zalogovan"
        typ_shody = "organicky_titulek_neni_zalogovan"
    results_match_str.append(match_str)
    results_match_len.append(match_len)
    results.append(typ_shody)
    # df_pd_cetnost_linky_api_title['novy'] = results_match_str
    # df_pd_cetnost_linky_api_title['novy1'] = results_match_len
    # df_pd_cetnost_linky_api_title['novy2'] = results

df_pd_cetnost_linky_api_title.to_csv('sequencematcher.csv', index = False)