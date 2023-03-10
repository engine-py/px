#!/usr/bin/env python3

# BoBoBo

import asyncio


async def handle_request(reader, writer, dispatch):
    # Initialize a buffer to store any leftover data from the previous request
    leftover_data = b''

    while True:
        # Read the incoming request data
        request_data = await reader.read()

        # If there is no data, the client has closed the connection, so we exit the loop
        if not request_data:
            break

        # Prepend any leftover data from the previous request
        request_data = leftover_data + request_data

        # Process the request data and split it into separate requests
        requests = []
        while request_data:
            # Check if there is a complete request in the data
            content_length = None
            if b'Content-Length: ' in request_data:
                index = request_data.find(b'Content-Length: ') + len(b'Content-Length: ')
                content_length = int(request_data[index:request_data.find(b'\r\n', index)])

            if content_length is None:
                # If there is no Content-Length header,
                # we assume there is only one request in the data
                requests.append(request_data)
                request_data = b''
            else:
                # Extract the next complete request from the data
                end_index = request_data.find(b'\r\n\r\n', content_length) + len(b'\r\n\r\n')
                if end_index == -1:
                    break
                requests.append(request_data[:end_index])
                request_data = request_data[end_index:]

        # If the last request is incomplete, store the leftover data for the next request
        if request_data:
            leftover_data = request_data

        # Process each request using the dispatch function
        for req in requests:
            response = generate_response(dispatch(req))
            writer.write(response)

            # Drain the writer to make sure all data is sent before continuing
            await writer.drain()

    # Close the connection to the client
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
