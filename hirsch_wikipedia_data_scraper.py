import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import datetime as dt
import os, re
from urllib.request import urlopen, Request

def scrape_wiki_edit_data(page):
    if not os.path.exists(f'./{page}.txt'):
        # create fake browser user
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        
        # url to get data from
        reg_url = f"https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{page}"
        
        # make request and download data
        req = Request(url=reg_url, headers=headers)
        html = urlopen(req).read()
        
        # get new line characters good
        s = ""
        for c in str(html):
            s += c
        s = s.split('\\n')
        
        # write to file
        with open(f'{page}.txt', 'w') as f:
            for line in s:
                f.write(line + '\n')
        
    lines = []
    with open(f'{page}.txt', 'r') as f:
        for line in f:
            lines.append(line)

    table_lines = []

    # grab monthly data table from html
    for i, line in enumerate(lines):
        if "table table-bordered table-hover table-striped month-counts-table" in line:
            j = i + 1
            while "</table>" not in lines[j]:
                table_lines.append(lines[j].strip())
                j += 1
            break
    
    columns = []
    data = {}

    p1 = re.compile('data-column=".*"')
    p2 = re.compile('".*"')

    for i, line in enumerate(table_lines):
        if "data-column" in line:
            x = p1.search(line).group(0)
            y = p2.search(x).group(0)[1:-1]
            columns.append(y)
            data[columns[-1]] = []
        
    patterns = [re.compile(f'class="sort-entry--{column}"') for column in columns]
    p3 = re.compile('data-value=".*"')
    p4 = re.compile('".*"')

    for i, line in enumerate(table_lines):
        for j, pattern in enumerate(patterns):
            if pattern.search(line) is not None:
                this_data = p3.search(line).group(0)
                this_data = p4.search(this_data).group(0)[1:-1]
                data[columns[j]].append(this_data)

    return data

def format_data(data):
    for i in range(len(data['month'])):
        month = data['month'][i]
        edits = data['edits'][i]
        data['month'][i] = dt.datetime(int(month[:4]), int(month[4:]), 1)
        data['edits'][i] = int(edits)
    df = pd.DataFrame(data)
    df['edits'] = df['edits']/max(df['edits'])*100
    df.fillna(0)

    return df

data = scrape_wiki_edit_data("National_Security_Agency")
nsa_wiki = format_data(data)
data = scrape_wiki_edit_data("Edward_Snowden")
snowden_wiki = format_data(data)

plt.plot(nsa_wiki['month'], nsa_wiki['edits'], label='NSA')
plt.plot(snowden_wiki['month'], snowden_wiki['edits'], label='Snowden')
plt.show()

nsa_google = pd.read_csv("nsa_search_trends.csv", skiprows=2)

compare_edits = pd.DataFrame({"Wiki": np.array(nsa_wiki[nsa_wiki['month'] >= dt.datetime(2004, 1, 1)]['edits']),
                             "Google": np.array(nsa_google['NSA: (United States)'])})
result = sm.ols(formula="Google ~ Wiki", data=compare_edits).fit()
print(result.params)
print(result.summary())

plt.scatter(nsa_wiki[nsa_wiki['month'] >= dt.datetime(2004, 1, 1)]['edits'], 
            nsa_google['NSA: (United States)'])
plt.plot([0, 100], [result.params['Intercept'], result.params['Intercept']+100*result.params['Wiki']])
plt.show()