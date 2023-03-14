#!/usr/bin/env python3

# BoBoBo

import sys
import argparse
import importlib
from .http_server import start
from . import context as pxctx


def parse_args():
    parser = argparse.ArgumentParser(description='Start a Px server.')

    parser.add_argument('-P', '--port', type=int, dest='port', default=8080, help='Port to listen on')
    parser.add_argument('-H', '--host', dest='host', default='localhost', help='Host to listen on')
    parser.add_argument('--static-resource', metavar='DIR',
                        dest='static_dir', default=None, help='Directory containing static resources')

    # The parameters --http and --wsgi are mutually exclusive, 
    # meaning only one of them can be used at a time.
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--http', dest='request_process_module',
                       help='module to handle HTTP requests')
    group.add_argument('--wsgi', dest='wsgi_app_module',
                       help='module to run a WSGI application')

    args = parser.parse_args()

    return args


def main():
    args = parse_command()

    if args.request_process_module:
        pxctx.setup_request_process_module(args.request_process_module)
    elif args.wsgi_process_module:
        pxctx.setup_wsgi_process_module(args.wsgi_app_module)
    else:
        pxctx.setup_default_process_module()

    start(args.host, args.port, pxctx.get_process_module())


if __name__ == '__main__':
    main()
