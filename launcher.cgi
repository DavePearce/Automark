#!/usr/bin/python

# ============================================================
# Imports
# ============================================================

import cgitb ; cgitb.enable()
import wsgiref.handlers
from wsgiref.simple_server import make_server

# ============================================================
# Path Config
# ============================================================

sys.path.insert(0, "lib")
sys.path.insert(0, ".")

# ============================================================
# Application Entry
# ============================================================

def application(environ, start_response):

   # Sorting and stringifying the environment key, value pairs
   response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
   response_body = '\n'.join(response_body)

   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   
   return [response_body]

# ============================================================
# Run Local HTTP Server
# ============================================================

httpd = make_server('localhost', 8051, application)
httpd.handle_request()
