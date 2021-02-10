# -*- coding: utf-8 -*-
"""
This script is an updated version of the DCD-Tool.py script. It is formatted for the cdi_master_update_2020.json file. The
script goes through the cdi master list and determines which links are working, broken, and the ones that have been dropped from CDI.
It produces a csv and six text files with this information while also printing it to the screen.
"""

# Import packages necessary for running code
import requests
import json
import urllib
import csv

# Retrieve "CDI Master List" from GitHub
github_json = urllib.request.urlopen("https://raw.githubusercontent.com/NASA-IMPACT/cdi_master/master/cdi_master_update_2020.json")

# Format json contents
first_api_opener = json.load(github_json)

# Initialize headers for the CSV output
fields = ['API URL', 'Title', 'Name', 'Catalog URL', 'CDI Theme']

# Initialize containers
broken_urls = []
working_urls = []
dropped_from_cdi = []
values_container = []
api_url_list = []
dropped_urls = []
dropped_themes = []
broken_titles = []
broken_themes = []

# Creating CSV of Dropped URLs with their necessary values
print('[*] Starting Code [*]\n[*] Building CSV Sheet [*]')
with open('CDI_Errors.csv', 'w', newline='') as outfile:
    csvwriter = csv.DictWriter(outfile, fieldnames = fields)
    csvwriter.writeheader()
    # Loops through the GitHub raw json file looking for API URLs
    for first_json in first_api_opener:
        api_url_list.append(first_json)
        #if first_json['api_url']:
        first_api = first_json['api_url']
        # If the API URL isn't healthy, it's reported
        if requests.get(first_api).status_code != 200:
            print('Found a broken link...')
            #broken_urls.append(first_api)
            broken_urls.append(first_json['catalog_url']) # dataset urls
            broken_titles.append(first_json['title']) # dataset titles
            broken_themes.append(first_json['cdi_themes']) # dataset theme tags
            csvwriter.writerow({'API URL': ('BROKEN: ' + first_api), 'Title': first_json['title'], 'Name': first_json['name'], 'Catalog URL': first_json['catalog_url'], 'CDI Theme': first_json['cdi_themes']})
        else:
            # If the API URL in the raw GitHub json is healthy,
            # the code continues looking for the *next* api url
            working_urls.append(first_api)
            if len(working_urls) % 10 == 0:
                print (len(working_urls))
            second_api_opener = urllib.request.urlopen(first_api)
            second_api = json.load(second_api_opener)
            # Within the json, the information we need is contained in a
            # next dictionary/loop format called "Groups"
            # Looks within "Groups" to check for the
            # key value, "climate5434". If no value is found,
            # the code reports it
            if not second_api['result']['groups'] or not any(d['name'] == 'climate5434' for d in second_api['result']['groups']):
                print (second_api['result']['groups'])
                dropped_from_cdi.append(second_api['result']['title']) # dataset titles
                dropped_urls.append(first_json['catalog_url']) # dataset urls
                dropped_themes.append(first_json['cdi_themes']) # dataset theme tags
                csvwriter.writerow({'API URL': first_api, 'Title': second_api['result']['title'], 'Name': second_api['result']['name'], 'Catalog URL': first_json['catalog_url'], 'CDI Theme': first_json['cdi_themes']})

# Create text files for Broken URLs and Dropped URLs
print('\n[*] Generating text files [*]')
with open('working_urls.txt', 'w') as outfile:
    for entry in working_urls:
        outfile.write(entry + '\n')
with open('broken_urls.txt', 'w') as outfile:
    for entry in broken_urls:
        outfile.write(entry + '\n')
with open('broken_titles.txt', 'w') as outfile:
    for entry in broken_titles:
        outfile.write(entry + '\n')
        
# reformatting list of themes for broken links        
broken_themes_1 = [x.replace('[\'["', '') for x in broken_themes]
broken_themes_2 = [x.replace('","', '; ') for x in broken_themes_1]
broken_themes_3 = [x.replace('"]\']', '') for x in broken_themes_2]
broken_themes_4 = [x.replace('"]\', None, \'["', "; ") for x in broken_themes_3]
broken_themes_5 = [x.replace('[None, \'["', '') for x in broken_themes_4]
broken_themes_6 = [x.replace('"]\', None]', '') for x in broken_themes_5]
broken_themes_regroup = [x.replace('"]\', \'["', '; ') for x in broken_themes_6]

with open('broken_themes.txt', 'w') as outfile:
    for entry in broken_themes_regroup:
        outfile.write(entry + '\n')
with open('dropped_from_cdi.txt', 'w') as outfile:
    for entry in dropped_from_cdi:
        outfile.write(entry + '\n')
with open('dropped_urls.txt', 'w') as outfile:
    for entry in dropped_urls:
        outfile.write(entry + '\n')
        
# reformatting list of themes for dropped links
dropped_themes_1 = [x.replace('[\'["', '') for x in dropped_themes]
dropped_themes_2 = [x.replace('","', '; ') for x in dropped_themes_1]
dropped_themes_3 = [x.replace('"]\']', '') for x in dropped_themes_2]
dropped_themes_4 = [x.replace('"]\', None, \'["', "; ") for x in dropped_themes_3]
dropped_themes_5 = [x.replace('[None, \'["', '') for x in dropped_themes_4]
dropped_themes_6 = [x.replace('"]\', None]', '') for x in dropped_themes_5]
dropped_themes_regroup = [x.replace('"]\', \'["', '; ') for x in dropped_themes_6]

with open('dropped_themes.txt', 'w') as outfile:
    for entry in dropped_themes_regroup:
        outfile.write(entry + '\n')

print("<!> COMPLETE <!>")
print("\n == List lengths == \n")
print('Total number of APIs pinged: ', len(api_url_list))
print('Total number of working URLs: ', len(working_urls))
print('Total number of broken URLs: ', len(broken_urls))
print('Total number of dropped URLs: ', len(dropped_from_cdi))
