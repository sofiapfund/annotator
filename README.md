# annotator

This repository contains all the scripts required to set up a local web server that allows the simple and fast annotation of scientific articles to populate the Progenetix publication collection. 

_The scripts:_

* __my_server.py__ launches a local web server, provides input fields to make annotations and uploads the newly created Progenetix posts on the publication collection.

* __my_html.py__ contains the html elements that describe the structure of the web page and the interactive form that collects the user's inputs. 

* __utils.py__ provides some predefined functions that are required for the generation of new posts for the publication collection, starting from the information found in the previously submitted annotations.  

_Goals:_
-  [ ] implement a 'post-updating' function (until now, only 'post-uploading' function): overwrite information for publications that are already in the Progenetix publication collection. This would be for example useful to add correct sample type annotations. 
-  [ ] improve form (autocomplete feature after PMID is given - for publications that are already in the collection)
