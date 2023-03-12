#!/usr/bin/env python3

# BoBoBo

import asyncio

def parse_http_request_line(request_line_bytes):
    line_str = request_line_bytes.decode('utf-8').strip()
    parts = line_str.split()

    if len(parts) != 3:
        raise ValueError("Invalid HTTP request line")
        
    method, path, version = parts
    return (method, path, version)


def parse_http_headers(headers_bytes):
    headers = {}
    lines = headers_bytes.decode().split(b'\r\n')
    for line in lines:
        if not line:
            continue
        key, value = line.split(': ', 1)
        headers[key] = value
    return headers


async def handle_request(reader, writer, process_module):
    # Initialize a buffer to store any leftover data from the previous request
    leftover_data = b''
    request_line = None
    headers = None
    body = None

    while True:
        request_data = await reader.read(1024)
        if not request_data:
            break
        request_data = leftover_data + request_data

        if request_line is None:
            request_line_end_index = request_data.find(b'\r\n')
            if request_line_end_index == -1:
                leftover_data = request_data
                continue
            else:
                try:
                    request_line = parse_http_request_line(request_data[:request_line_end_index])
                    request_data = request_data[request_line_end_index + 2: ]
                    res = process_module.filter_request_line(request_line)
                except Exception as ex:
                    logger.error('Error with request line')
                    break
                else:
                    if not res is None:
                        response = generate_response(res)
                        writer.write(response)
                        await writer.drain()
                        break

        if request_line is not None and headers is None:
            headers_end_index = request_data.find(b'\r\n\r\n')
            if headers_end_index == -1:
                leftover_data = request_data
                continue
            else:
                headers_bytes = request_data[:headers_end_index]
                headers = parse_http_headers(headers_bytes)
                request_data = request_data[headers_end_index + 4: ]
                try:
                    res = process_module.filter_headers(headers)
                except Exception as ex:
                    break
                else:
                    if not res is None:
                        response = generate_response(res)
                        writer.write(response)
                        await writer.drain()
                        break

        if headers is not None and body is None:
            content_length = headers.get('content_length', None)
            
            if content_length is None:
                body = request_data
            else:
                if len(request_data) < content_length:
                    leftover_data = request_data
                    continue
                else:
                    content_length = int(content_length)
                    body = request_data[:content_length]
                    request_data = request_data[content_length:]
                    try:
                        res = process_module.dispatch(request_line, headers, body)
                        request_line = None
                        headers = None
                        body = None
                    except Exception as ex:
                        break
                    else:
                        if not res is None:
                            response = generate_response(res)
                            writer.write(response)
                            await writer.drain()

    writer.close()


def generate_response(response):
    status_line = f'HTTP/1.1 {response["status"]}\r\n'
    header_lines = [f'{k}: {v}\r\n' for k, v in response['headers'].items()]
    headers = ''.join(header_lines)
    body = response['body'] if isinstance(response['body'], bytes) else response['body'].encode()
    response_data = f'{status_line}{headers}\r\n{body.decode()}'.encode()
    return response_data


async def run_server(dispatch, host, port):
    # Create the server
    server = await asyncio.start_server(lambda r, w: handle_request(r, w, dispatch),
                                        host=host, port=port)

    # Keep the server running
    async with server:
        await server.serve_forever()


def start(dispatch, host='127.0.0.1', port=8080):
    asyncio.run(run_server(dispatch, host, port))
