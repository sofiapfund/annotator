#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, CGIHTTPRequestHandler
import cgi
import os
from os import path

# Local
dir_path = path.dirname( path.abspath(__file__) )
os.chdir(dir_path)

from utils import create_progenetix_posts, upload_publication, jprint
from my_html import landing_page, form


'''

`Progenetix publications annotator`
Once the server is running, more than one publication can be annotated and will automatically be inserted into
progenetix.publications. When annotating, follow the instructions provided on the local website.
After usage, remember to stop the server from running with [ctrl]-c.

'''

hostName = "localhost"
serverPort = 8030

class MyServer(CGIHTTPRequestHandler):

    def do_GET(self):

        if self.path.endswith("/annotator"):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            self.wfile.write(landing_page.encode(encoding='utf_8'))
            return

        if self.path.endswith("/new"):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            self.wfile.write(form.encode(encoding='utf_8'))
            return


    def do_POST(self):
            try:
                if self.path.endswith("/new"):
                    print(self.path)
                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/annotator')
                    self.end_headers()

                    form = cgi.FieldStorage(fp=self.rfile,
                                            headers=self.headers,
                                            environ={
                                            'REQUEST_METHOD': 'POST',
                                            'CONTENT_TYPE': self.headers['Content-Type'],
                                            })

                    d = {}
                    params = ['pmid', 'acgh', 'ccgh', 'wes', 'wgs', 'provenance_id', 'sample_types', 'status', 'note']
                    for p in params:
                        d[p] = form.getvalue(p) # e.g., pmid = form.getvalue['pmid']

                    # Generate new post for the Progenetix publication collection
                    new_post = create_progenetix_posts(d)
                    print("\nThis is my new post for the Progenetix publication collection:")
                    jprint(new_post)
                    print("\n... Uploading new post to the collection ...\n")

                    # Upload post in the MongoDB Progenetix publication collection (if new):
                    upload_publication(new_post)
                    return

            except:
                pass


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s/annotator" % (hostName, serverPort))
    print("Use [ctrl]-c to terminate.")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
