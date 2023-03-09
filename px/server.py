#!/usr/bin/env python3

# BoBoBo

import socket
import select


def start(host, port, backlog, route):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(backlog)
    epoll = select.epoll()
    start_epoll(epoll, server_socket, route)

def start_select(epoll, server_socket, route):
    epoll.register(server_socket.fileno(), select.EPOLLIN)

    SIZE = 1024
    connections = {}
    requests = {}
    responses = {}
    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == server_socket.fileno():
                client_socket, client_address = server_socket.accept()
                epoll.register(client_socket.fileno(), select.EPOLLIN)
                connections[client_socket.fileno()] = client_socket
                requests[client_socket.fileno()] = b''

            elif event & select.EPOLLIN:
                data = connections[fileno].recv(SIZE)
                
                if not data:
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
                    del requests[fileno]
                    del responses[fileno]
                    continue
                
                requests[fileno] += data
                
                if b'\r\n\r\n' in requests[fileno]:
                    headers, body = requests[fileno].split(b'\r\n\r\n', 1)
                    
                    content_length = None
                    for header in headers.decode().split('\r\n')[1:]:
                        if header.lower().startswith('content-length:'):
                            content_length = int(header.split(':')[-1].strip())
                    
                    if content_length is not None:
                        if len(body) < content_length:
                            continue
                        else:
                            body = body[:content_length]
                                        
                    req = headers + b'\r\n\r\n' + body
                    requests[fileno] = req
                    logger.debug(req)

                    # What to do with the http request
                    # How to send response
                    route(req, response_to(fileno))
                    
            elif event & select.EPOLLOUT:
                bytes_sent = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][bytes_sent:]
                
                if len(responses[fileno]) == 0:
                    epoll.modify(fileno, 0)
                    connections[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
                del requests[fileno]
                del responses[fileno]

def close():
    epoll.unregister(server_socket.fileno())
    epoll.close()
    server_socket.close()
