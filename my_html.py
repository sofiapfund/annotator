#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os import path

# Local
dir_path = path.dirname( path.abspath(__file__) )
os.chdir(dir_path)

# Style
font = 'font-family:"Helvetica"'

# EPMC Query 
query = 'https://europepmc.org/search?query=%28whole%20genome%20sequencing%20OR%20whole%20exome%20sequencing%20OR%20%28array%20AND%20genomic%29%20OR%20%28SNP%20AND%20array%29%20OR%20comparative%20genomic%20hybridization%20AND%20%28cancer%20OR%20leukemia%20OR%20lymphoma%29%29%20AND%20%28%28%28SRC%3AMED%20OR%20SRC%3APMC%20OR%20SRC%3AAGR%20OR%20SRC%3ACBA%29%20NOT%20%28PUB_TYPE%3A%22Review%22%29%29%29%20AND%20%28%28%28SRC%3AMED%20OR%20SRC%3APMC%20OR%20SRC%3AAGR%20OR%20SRC%3ACBA%29%20NOT%20%28PUB_TYPE%3A%22Review%22%29%29%29&page=1&sortBy=FIRST_PDATE_D%2Bdesc'

# Main page
landing_page = ""
landing_page += f"<html><body style={font}>"
landing_page += "<h1>Publication Annotator</h1>"
landing_page += ("<p>This web server can be used as a tool to annotate information from scientific publications to populate the " +
                        "<a href='https://progenetix.org/' target='_blank'>Progenetix</a> cancer genome database.</p><br>")
landing_page += ("<fieldset><h4><strong>Step 1</strong> - Make a query on Europe PMC by clicking " +
                 f"<a href={query} target='_blank'>here</a>.</h4></fieldset>")
landing_page += "<fieldset><h4><strong>Step 2</strong> - Annotate relevant scientific publications by clicking <a href='/annotator/new'>here</a>.</h4></fieldset><br>"
landing_page += "<p> To check the <strong>criteria of inclusion</strong> in the Progenetix publication collection, consult the following <a href='https://info.progenetix.org/doc/publication-collection.html' target='_blank'>webpage.</a></p>"
landing_page += "</body></html>"

# Form
form = ""

form += f"<html><body style={font}>"
form += "<h1>New Annotations</h1>"

form += "<form method = 'POST' enctype='multipart/form-data' action='/annotator/new'>"

form += "<fieldset><p><strong>PMID</strong>: PubMed ID of the publication, e.g. <em>12345678</em></p>"
form += "<input name = 'pmid' type = 'number' placeholder='12345678'></fieldset>"

form += "<fieldset><p><strong>aCGH</strong>: number of array copy genomic hybridization samples in the publication, e.g. <em>23</em></p>"
form += "<input name = 'acgh' type = 'number' placeholder='23'></fieldset>"

form += "<fieldset><p><strong>cCGH</strong>: number of copy genomic hybridization samples in the publication, e.g. <em>0</em></p>"
form += "<input name = 'ccgh' type = 'number' placeholder='0'></fieldset>"

form += "<fieldset><p><strong>WES</strong>: number of samples analyzed with whole-exome sequencing in the publication, e.g. <em>77</em></p>"
form += "<input name = 'wes' type = 'number' placeholder='77'></fieldset>"

form += "<fieldset><p><strong>WGS</strong>: number of samples analyzed with whole-genome sequencing in the publication, e.g. <em>5</em></p>"
form += "<input name = 'wgs' type = 'number' placeholder='5'></fieldset>"

form += "<fieldset><p><strong>Provenance ID</strong>: first author's affiliation location ID given as <em>city::country</em>. "
form += "Check for possible provenance IDs on this <a href ='https://progenetix.org/services/geolocations/?city=heidelberg' target='_blank'>link</a> by changing the name of the city of interest.</p> "
form += "<input name = 'provenance_id' type = 'text' placeholder='heidelberg::germany'></fieldset>"

form += ("<fieldset><p><strong>Sample Types</strong>: <a href='https://progenetix.org/subsets/biosubsets/' target='_blank'>NCIT code</a>" +
            " of the analyzed tumor type <strong>and</strong> number of such samples (comma- and semincolon-separated), e.g. <em>C4911, 77; C4349, 23</em></p>")
form += "<input name = 'sample_types' type = 'text' placeholder='C4911, 105'></fieldset>"

form += "<fieldset><p><strong>Status</strong>: gives information about the publication or the reason of its exclusion.</p>"
form += ('<select name="status" id="status">' +
            '<option value="">--Please choose an option--</option>'+
            '<option value="Sample data in Progenetix.">Sample data in Progenetix.</option>'+
            '<option value="Sample data not accessible.">Sample data not accessible.</option>'+
            '<option value="Excluded[non-cancer]">Excluded[non-cancer]</option>'+
            '<option value="Excluded[animal model]">Excluded[animal model]</option>'+
            '<option value="Excluded[not whole genome]"> Excluded[not whole genome]</option>'+
            '<option value="Excluded[not whole genome]"> Excluded[technical]</option>'+
            '<option value="Excluded[review]">Excluded[review]</option></select></fieldset>')

form += "<fieldset><p><strong>Comments</strong>: write additional information about the publication, e.g. <em>international samples</em></p>"
form += "<input name = 'note' type = 'text' placeholder='...'></fieldset>"

form += "<input type = 'submit' value = 'Submit'>"
form += "</form>"
form += "</body></html>"

