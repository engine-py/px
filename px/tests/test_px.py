#!/usr/bin/env python3

# BoBoBo

import unittest
import asyncio
import http.client
from px.main import main


class PxServerTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_server_start_with_defaults(self):
        app = server.PxApp()
        server_task = asyncio.ensure_future(app.start_server())
        self.loop.run_until_complete(asyncio.sleep(0.1))  # wait for server to start

        conn = http.client.HTTPConnection('localhost', port=8080)
        conn.request('GET', '/')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertEqual(response.read(), b'Hello, world!')

        server_task.cancel()
        self.loop.run_until_complete(server_task)  # wait for server to stop

    def test_server_start_with_custom_host_and_port(self):
        app = server.PxApp(host='127.0.0.1', port=8888)
        server_task = asyncio.ensure_future(app.start_server())
        self.loop.run_until_complete(asyncio.sleep(0.1))  # wait for server to start

        conn = http.client.HTTPConnection('127.0.0.1', port=8888)
        conn.request('GET', '/')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertEqual(response.read(), b'Hello, world!')

        server_task.cancel()
        self.loop.run_until_complete(server_task)  # wait for server to stop

    def test_server_start_with_static_resource_dir(self):
        app = server.PxApp(static_dir='static')
        server_task = asyncio.ensure_future(app.start_server())
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
        app = server.PxApp(wsgi_app='tests.test_wsgi_app')
        server_task = asyncio.ensure_future(app.start_server())
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
