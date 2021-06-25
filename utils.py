#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import re
#from isodate import date_isoformat
from pymongo import MongoClient
import os
from os import path

# Local
dir_path = path.dirname( path.abspath(__file__) )
os.chdir(dir_path)

##############################################################################
##############################################################################
##############################################################################

def jprint(obj):
    text = json.dumps(obj, sort_keys= True, indent = 4, ensure_ascii = False)
    print(text)

##############################################################################

def retrieve_epmc_publications(pmid): # d['pmid'] as an input

    parameters = {
        "query": "ext_id:" + pmid,
        "format": "json",
        "resultType": "core"
        }
    response = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params = parameters)

    if response.status_code == 200:
        results = response.json()["resultList"]["result"] # it's a list containing one dictionary

    return results[0] # it's a dictionary

##############################################################################

def create_short_publication_label(author, title, year):

    short_author = re.sub(r'(.{2,32}[\w\.\-]+? \w\-?\w?\w?)(\,| and ).*?$', r'\1 et al.', author)

    if len(title) <= 100:
        label = short_author + f' ({year}) ' + title
    else:
        label = short_author + f' ({year}) ' + ' '.join(title.split(' ')[:12]) + ' ...'

    return label

##############################################################################

def get_geolocation(locationID): #heidelberg::germany

   location = requests.get(f"https://progenetix.org/cgi/bycon/services/geolocations.py?id={locationID}")
   coordinates = location.json()["response"]["results"]

   return coordinates

##############################################################################

def get_ncit_tumor_type(tumors):

    # Convert "tumors" in a list containing [[ncit, counts], [ncit, counts], ...]
    types = tumors.split('; ') # if >1 tumor type is present, information must be separated by "; "
    list_types = []
    for t in types:
        typ = t.split(', ')
        list_types.append(typ)

    # Get full names of tumors
    names = []
    for typ in list_types:
        ncit = typ[0]
        url = f'https://progenetix.org/services/collations?filters=NCIT:{ncit}&method=counts&responseType=json'
        response = requests.get(url)
        data = response.json()
        tumor_name = data['response']['results'][0]['label']
        names.append(tumor_name)

    # Fill in sample_types list
    sample_types = []
    for i, typ in enumerate(list_types):
        tumor_type = {}
        ID = "NCIT:" + typ[0]
        counts = int(typ[1])
        tumor_type.update({"id": ID,
                           "label": names[i],
                           "counts": counts,
                           })
        tumor_copy = tumor_type.copy()
        sample_types.append(tumor_copy)

    return sample_types

##############################################################################

def create_progenetix_posts(dictionary): # dictionary of the required parameters (pmid, acgh, etc.)

    post = {}

    informations = retrieve_epmc_publications(dictionary['pmid'])

    if informations != None: # only if publication PMID matched the query
        abstract = informations["abstractText"]
        ID = informations["pmid"]
        author = informations["authorString"]
        journal = informations["journalInfo"]["journal"]["medlineAbbreviation"]
        title = informations["title"]
        year = informations["pubYear"]

        # Remove HTML formatting:
        abstract_no_html = re.sub(r'<[^\>]+?>', "", abstract)
        title_no_html = re.sub(r'<[^\>]+?>', "", title)
        abstract, title = abstract_no_html, title_no_html

        # Fill in counts:
        counts = {}
        counts.update({"acgh": int(dictionary['acgh']),
                        "arraymap": 0,
                        "ccgh": int(dictionary['ccgh']),
                        "genomes": int(dictionary['acgh']) + int(dictionary['ccgh']) + int(dictionary['wes']) + int(dictionary['wgs']), # tot nr of tumor samples
                        "ngs": int(dictionary['wes']) + int(dictionary['wgs']), # tot nr of tumor samples analyzed with NGS techniques
                        "progenetix": 0,
                        "wes": int(dictionary['wes']),
                        "wgs": int(dictionary['wgs'])
                         })

        post.update({"abstract": abstract,
                    "authors": author,
                    "counts": counts,
                    "id": "PMID:" + str(ID),
                    "label": create_short_publication_label(author, title, year),
                    "journal": journal,
                    "provenance": get_geolocation(str(dictionary['provenance_id'])),
                    "sample_types": get_ncit_tumor_type(dictionary['sample_types']),
                    "sortid": None,
                    "title": title,
                    "year": year
                    })

    return post

##############################################################################

def upload_publication(post):

    client = MongoClient()
    cl = client['progenetix'].publications
    ids = cl.distinct("id")

    if post["id"] in ids:
        print(post["id"], ": skipped - already in progenetix.publications\n")
    else:
        print(post["id"], ": inserting this into progenetix.publications\n")
        #post.update( { "updated": date_isoformat(datetime.datetime.now()) } )
        result = cl.insert_one(post)
        result.inserted_id

#test = {'pmid': '34103027', 'acgh': '0', 'ccgh': '0', 'wes': '0', 'wgs': '0', 'provenance_id': 'nanning::china', 'sample_types': 'C3099, 75', 'status': 'Sample data in Progenetix.', 'note': 'none'}
#post = create_progenetix_posts(test)
#upload_publication(post)

##############################################################################
##############################################################################
##############################################################################
