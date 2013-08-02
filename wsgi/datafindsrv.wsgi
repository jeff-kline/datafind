#!/usr/bin/python
# -*- Python -*-
from wsgiref.util import setup_testing_defaults
import sys

DEBUG=False

def app(environ, start_response):
    if DEBUG:
        setup_testing_defaults(environ)

    try:
        status = "200 OK"
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        # return ['OK']
        raise RuntimeError('Froody!')
    except:
        status = "500 Fail"
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers, exc_info=sys.exc_info())
        return ['Fail']

if __name__=="__main__":
    from wsgiref.simple_server import make_server
    # DEBUG=True
    httpd = make_server('', 8000, app)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()
