#!/usr/bin/env python3

# BoBoBo

from boon.web.wsgi import parse_request_environ
from .context import PxContext

async def dispatch(request_line, headers, body):
    """
    Dispatch http request by WSGI
    """
    environ = parse_request_environ(request_line, headers, body)
    resp = {}

    def start_response(status, response_headers):
        nonlocal resp
        resp['status'] = status
        resp['headers'] = response_headers

    wsgi_app = PxContext.get_wsgi_app()
    res = wsgi_app(environ, start_response)
    resp['body'] = res

    return resp
