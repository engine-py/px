#!/usr/bin/env python3

# BoBoBo

import unittest
import asyncio
import http
from unittest.mock import patch
from px.main import main


class PxServerTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.host = '127.0.0.1'
        self.port = 8888

    def tearDown(self):
        self.loop.close()

    def test_with_defaults(self):
        with patch('sys.argv', ['px', '-H', self.host, '-P', str(self.port)]):
            main()
            self.loop.run_until_complete(asyncio.sleep(0.1))  # wait for server to start

        conn = http.client.HTTPConnection(self.host, port=8080)
        conn.request('GET', '/')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertEqual(response.read(), b'Hello, world!')

    def test_server_start_with_custom_host_and_port(self):
        with patch('sys.argv', ['px', '-H', self.host, '-P', str(self.port)]):
            server_task = asyncio.ensure_future(main)
            self.loop.run_until_complete(asyncio.sleep(0.1))  # wait for server to start

        conn = http.client.HTTPConnection(self.host, port=self.port)
        conn.request('GET', '/')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertEqual(response.read(), b'Hello, world!')

        server_task.cancel()
        self.loop.run_until_complete(server_task)  # wait for server to stop

    def test_server_start_with_static_resource_dir(self):
        with patch('sys.argv', ['px', '-H', self.host, '-P', str(self.port), '--static-resource', self.static_dir]):
            server_task = asyncio.ensure_future(main)
            self.loop.run_until_complete(asyncio.sleep(0.1))  # wait for server to start

        conn = http.client.HTTPConnection('localhost', port=8080)
        conn.request('GET', '/static/test.txt')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertEqual(response.read(), b'This is a test file.\n')

        server_task.cancel()
        self.loop.run_until_complete(server_task)  # wait for server to stop

    def test_server_start_with_wsgi_app_module(self):
        with patch('sys.argv', ['px', '-H', self.host, '-P', str(self.port), '--wsgi', self.wsgi_app_module]):
            server_task = asyncio.ensure_future(main)
            self.loop.run_until_complete(asyncio.sleep(0.1))  # wait for server to start

        conn = http.client.HTTPConnection('localhost', port=8080)
        conn.request('GET', '/?name=John')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertEqual(response.read(), b'Hello, John!')

        server_task.cancel()
        self.loop.run_until_complete(server_task)  # wait for server to stop


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
