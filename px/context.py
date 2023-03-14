#!/usr/bin/env python3

# BoBoBo

PxContext = {}

def get_process_module():
    return PxContext['process_module']

def setup_process_module(m):
    PxContext['process_module'] = m

def put_wsgi_app(app):
    PxContext['wsgi_app'] = app

def get_wsgi_app(app):
    return PxContext['wsgi_app']


def create_default_process_module():
    from .example import process_module_example as m
    setup_process_module(m)


def create_http_process_module(process_request_module):
    module = importlib.import_module(process_request_module)
    setup_process_module(module)


def create_wsgi_process_module(wsgi_app_module):
    app_m = importlib.import_module(wsgi_app_module)
    if not hasattr(app_m, 'wsgi_app'):
        raise ValueError('Module %s does not have a wsgi_app function.' % wsgi_app_module)

    app = app_m.wsgi_app()
    put_wsgi_app(app)

    from . import wsgi_process_module as m
    setup_process_module(m)
