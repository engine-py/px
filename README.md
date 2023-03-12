# Px Server

Async HTTP Server in Python, and it`s functional.

## Usage

To start the server, use the following command:

```
python -m px -h <host> -p <port> -m <process_request_module> -d <static_resource_dir>
```

By default, the server listens on localhost:8080. 
You can specify a custom module to handle HTTP requests with the process_request_module argument.
The static_resource_dir argument defines the root path of the static resource directory.

Here is an example of a custom HTTP request processing module:

```
async def filter_request_line(request_line):
    # process the request line
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }

async def filter_headers(headers):
    # process the headers
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }

async def dispatch(request_line, headers, body):
    # process the request
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }

async def filter_response(response):
    # process the response
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }
```

The process_request_module is a custom module that defines three functions for processing an HTTP request:
filter_request_line(), filter_headers(), and dispatch().

The filter_request_line() function takes in the request line as a tuple parameter (method, path, version) 
and returns a dictionary 
that contains the HTTP response status, headers, and body. This function is responsible for filtering 
and processing the request line and returning an appropriate response.

The filter_headers() function takes in the HTTP headers as a dictionary parameter and returns a dictionary 
that contains the HTTP response status, headers, and body. This function is responsible for filtering 
and processing the HTTP headers and returning an appropriate response.

The dispatch() function takes in the request line, headers, and body as parameters and returns a dictionary 
that contains the HTTP response status, headers, and body. This function is responsible for dispatching 
the HTTP request to the appropriate handler based on the request method and URI path, processing the request, 
and returning an appropriate response.

All three functions should return a dictionary with the following keys:

* status: The HTTP response status code and reason phrase, e.g. "200 OK".
* headers: A dictionary of HTTP response headers, 
where the keys are the header names and the values are the header values.
* body: The HTTP response body, which can be a string or bytes object.

By defining these three functions in your process_request_module, 
you can customize the processing of incoming HTTP requests to your server.

## Testing

To test the server, you can use a tool like curl. For example:

```
$ curl http://localhost:8080/
Hello, World!
```

## License

This code is released under the GPL3 License. See LICENSE for more information.
