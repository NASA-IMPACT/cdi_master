# -*- coding: utf-8 -*-
"""
This script is a python version of the resilienceQA.R script on github. The script cross checks the 2020 CDI master list and
the Resilience community datasets. It produces a csv (ResilienceQA.csv) with two columns: 
    
    1. entries that are in the resilience community but not in the master list 
    2. entries that are in the master list but not in the resilience community
    
"""

# Import packages necessary for running code
import requests
import json
import urllib
import csv
from itertools import zip_longest

# Retrieve "CDI Master List" from GitHub and the Resilience community datasets
github_json = urllib.request.urlopen("https://raw.githubusercontent.com/NASA-IMPACT/cdi_master/master/cdi_master_update_2020.json")
resilience_json = urllib.request.urlopen("https://ual.geoplatform.gov/api/communities/4eebc494059beab9fda54cb078927ddc/items?type=dcat:Dataset&size=500")

# Format json contents
CDI_list = json.load(github_json)
Resilience_list = json.load(resilience_json)

# create empty lists for looping and appending
cdi_ids = []
resilience_ids = []
resilience_not_master = []
master_not_resilience = []

# loop through master list to remove ids listed as 'Not Available' and append ids that exist to cdi_ids
for entries in CDI_list:
    if entries['geoplatform_id'] != 'Not Available':
        cdi_ids.append(entries['geoplatform_id'])

# loop through resilience community to append ids to a list    
results = Resilience_list['results']
for result in results:
    resilience_ids.append(result['id'])
    
# loop through resilience community ids to determine which ones are missing from the cdi_ids
for rID in resilience_ids:
    if rID not in cdi_ids:
        resilience_not_master.append(rID)

# loop through cdi_ids to determine which ones are missing from the resilience community        
for cID in cdi_ids:
    if cID not in resilience_ids:
        master_not_resilience.append(cID)

# Building csv        
Resilience_QA = [resilience_not_master, master_not_resilience]
export_data = zip_longest(*Resilience_QA, fillvalue = '')
with open('ResilienceQA.csv','w', encoding = "ISO-8859-1", newline = '') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("ResilienceNotMaster", "MasterNotResilience"))
    wr.writerows(export_data)
myfile.close()
        
    