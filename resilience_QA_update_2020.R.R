#This is an update of resilience_QA.R to run on the updated master list
#This script takes the unique geoplatform id's and matches them straight from the Resilience community to the updated master list (cdi_master_update_2020.json) on Github.
#Manual curation will be needed once you obtain which id's are missing from the master list by checking the id in object editor.


#read in library needed for reading json files
library(RJSONIO)

#Make new vectors for dataset ids from Geoplatform
dataset_id <- c()


#Make a list of all tagged datasets within the Resilience Community
datasets <- fromJSON("https://ual.geoplatform.gov/api/communities/4eebc494059beab9fda54cb078927ddc/items?type=dcat:Dataset&size=500")

#Loop through and grab the id from the datasets
for(j in 1:length(datasets[[1]])){
  dataset_id[j] <- datasets[[1]][[j]][['id']]
}

#From the cdi_master.json, make a new list of all of the cdi datasets
master_list <- fromJSON("https://raw.githubusercontent.com/NASA-IMPACT/cdi_master/master/cdi_master_update_2020.json")

#Make a new vector of gp_ids from the master document
master_id <- c()

#Populate titles of master document into new vector
for(k in 1:length(master_list)){
  master_id[k] <- master_list[[k]][[9]]
}

#creates a new vector where the id's are check for matches. a no match results in NA. NA means it is in resilience community but not in master list.
# if we want NA to mean it is in master list and not in resilience community, use: unmatched <- match(master_id, dataset_id, nomatch = NA)
unmatched <- match(dataset_id, master_id, nomatch = NA)
#if NA, take the position and check using " dataset_id['position #'] " and taking that ID into object editor.
#take that dataset back into the master list, and edit accordingly by either correcting the master list
#or correcting which dataset is linked to the resilience portfolio

