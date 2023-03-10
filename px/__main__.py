#!/usr/bin/env python3

# BoBoBo

import argparse
from .http_server import start


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Async HTTP Server')
    parser.add_argument('-p', '--port', type=int, default=8080, help='the port to listen on')
    parser.add_argument('-h', '--host', type=str, default='localhost', help='the host to bind to')
    args = parser.parse_args()

    # Define the dispatch function
    async def dispatch(request):
        return {
            'status': '200 OK',
            'headers': {
                'Content-Type': 'text/plain',
            },
            'body': 'Hello, World!',
        }

    start(dispatch, args.host, args.port)


if __name__ == '__main__':
    main()
