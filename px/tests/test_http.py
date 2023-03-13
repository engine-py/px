#!/usr/bin/env python3

# BoBoBo

import unittest
from px.http import parse_http_headers, parse_http_request_line, generate_response


class TestParseHttpRequestLine(unittest.TestCase):

    def test_valid_request_line(self):
        request_line = b"GET /index.html HTTP/1.1\r\n"
        expected_result = ("GET", "/index.html", "HTTP/1.1")
        result = parse_http_request_line(request_line)
        self.assertEqual(result, expected_result)

    def test_invalid_request_line(self):
        request_line = b"POST /index.php HTTP/1.2\r\n"
        with self.assertRaises(ValueError):
            parse_http_request_line(request_line)

    def test_empty_request_line(self):
        request_line = b"\r\n"
        with self.assertRaises(ValueError):
            parse_http_request_line(request_line)

    def test_missing_space_between_parts(self):
        request_line = b"GET/index.htmlHTTP/1.1\r\n"
        with self.assertRaises(ValueError):
            parse_http_request_line(request_line)

    def test_extra_spaces_between_parts(self):
        request_line = b"GET  /index.html  HTTP/1.1\r\n"
        expected_result = ("GET", "/index.html", "HTTP/1.1")
        result = parse_http_request_line(request_line)
        self.assertEqual(result, expected_result)

    def test_parse_http_headers(self):
        # Test basic case with one header
        headers_bytes = b'Content-Type: text/html\r\n'
        expected_output = {'Content-Type': 'text/html'}
        self.assertEqual(parse_http_headers(headers_bytes), expected_output)

        # Test case with multiple headers and a blank line
        headers_bytes = b'Content-Type: text/html\r\nServer: Apache\r\n\r\n'
        expected_output = {'Content-Type': 'text/html', 'Server': 'Apache'}
        self.assertEqual(parse_http_headers(headers_bytes), expected_output)

    def test_generate_response(self):
        # Test basic case with only status and body
        response = {'status': 200, 'body': 'Hello, World!'}
        expected_output = b'HTTP/1.1 200 OK\r\n\r\nHello, World!'
        self.assertEqual(generate_response(response), expected_output)

        # Test case with headers and non-ASCII characters in body
        response = {'status': 404, 'headers': {'Content-Language': 'fr'}, 
                    'body': u'Page non trouvée'.encode('utf-8')}
        expected_output = (b'HTTP/1.1 404 Not Found\r\nContent-Language: fr\r\n'
                           b'\r\nPage non trouv\xc3\xa9e')
        self.assertEqual(generate_response(response), expected_output)


if __name__ == '__main__':
    unittest.main()
