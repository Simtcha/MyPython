from optparse import IndentedHelpFormatter
from requests_html import HTMLSession
import csv

def get_data(s, url):
    r = s.get(url)
    return r.html.find('div.job_seen_beacon'), r.html.find('ul.pagination-list a[aria-label=Next]')

def parse_html(html):
    job = {
        'title': html.find('h2 > a')[0].text,
        'link': 'https://https://cz.indeed.com/viewjob?jk=' + html.find('h2 > a')[0].attrs['data-jk'],
        'company_name': html.find('span.companyInfo')[0],
        'snippet': html.find('div.job-snippet')[0],
    }

    try:
        job['salary'] = html.find('div.metadata.salary-snippet-container')[0].text
    except IndexError as err:
        # print(err)
        job['salary'] ='None Given'

    return job

def export(results):
    keys = results[0].keys()
    with open('results.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(resuts)



def main():
    results = []
    session = HTMLSession()
    base_url = 'https://cz.indeed.com'
    url = base_url + '/jobs?q=python+junior&from=searchOnHP&redirected=1&vjk=ffc9da0b629c4e65'
    
    while True:
        jobs = get_data(session, url)

        for job in jobs:
            results.append(parse_html(job))
        try:
            url = base_url + jobs[1][0].attrs['href']
            print(url)
        except IndexError as err:
            print(err)
            break

export(results)

if __name__ == '__main__':
    main()

