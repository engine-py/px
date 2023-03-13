#!/usr/bin/env python3

# BoBoBo

import asyncio
from .http import parse_http_request_line, parse_http_headers, generate_response


async def filter_and_send_response(resp, writer, process_module):
    """Filter response using process_module and send it to client.

    Args:
        response: The response to filter.
        writer: The StreamWriter to send the response to.
        process_module: The module containing the filter_response function.

    Returns:
        None
    """
    filtered_resp = process_module.filter_response(resp)
    response = generate_response(filtered_resp)
    writer.write(encoded_response)
    await writer.drain()


async def read_until(
    read_buffer: bytes,
    reader: asyncio.StreamReader,
    until_bytes: bytes
) -> Tuple[bytes, bytes]:
    """
    Read bytes by reader, until reach the until_bytes.
    Parameter read_buffer is used for caching bytes between multi-reads.
    """
    if not read_buffer:
        read_buffer = b''

    while True:
        data = await reader.read(1024)

        if not data:
            # End of stream reached, return whatever we've got so far
            return (b'', read_buffer)

        read_buffer += data

        end_index = read_buffer.find(until_bytes)
        if end_index != -1:
            # Found the delimiter, return the message and remaining buffer
            return (read_buffer[:end_index], read_buffer[end_index+len(until_bytes):])


async def handle_request(reader, writer, process_module):
    """
    Parse HTTP request bytes to request line, headers and body.
    Filter by request line and headers.
    Dispatch with http request.
    And filter response before return to client.
    """
    request_line = None
    headers = {}
    body = None

    read_buffer = b''
    while True:
        request_line_bytes, read_buffer = await read_until(read_buffer, reader, b'\r\n')
        request_line = parse_http_request_line(request_line_bytes)
        resp = process_module.filter_request_line(request_line)
        if resp:
            await filter_and_send_response(resp, writer, process_module)
            break

        headers_bytes, read_buffer = await read_until(read_buffer, reader, b'\r\n\r\n')
        headers = parse_http_headers(headers_bytes)
        resp = process_module.filter_headers(headers)
        if resp:
            await filter_and_send_response(resp, writer, process_module)
            break

        content_length = headers.get('content_length', None)
            
        while True:
            if content_length is None:
                body = read_buffer
            else:
                if len(read_buffer) < content_length:
                    data = await reader.read(1024)
                    if not data:
                        writer.close()
                        return
                    read_buffer = read_buffer + data
                    continue
                else:
                    content_length = int(content_length)
                    body = read_buffer[:content_length]

            resp = process_module.dispatch(request_line, headers, body)
            if resp:
                await filter_and_send_response(resp, writer, process_module)
                break

    writer.close()


async def run_server(dispatch, host, port):
    # Create the server
    server = await asyncio.start_server(lambda r, w: handle_request(r, w, dispatch),
                                        host=host, port=port)

    # Keep the server running
    async with server:
        await server.serve_forever()


def start(dispatch, host='127.0.0.1', port=8080):
    asyncio.run(run_server(dispatch, host, port))
