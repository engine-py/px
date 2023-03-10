# px

Async HTTP Server in Python

The server uses asyncio and functional programming to process incoming requests.

## Usage

To start the server, run the following command:

```
python -m px -h localhost -p 8080
```

By default, the server listens on localhost:8080. 

To process incoming requests, you need to provide a dispatch function that takes a request object and returns a response object.

Here's an example dispatch function:

```
async def dispatch(request):
    # Process the request
    # ...

    # Return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }
```

The dispatch function takes a single argument, request, which is a dictionary that contains the following keys:

```
method: The HTTP method (e.g., 'GET', 'POST', etc.).
path: The request path (e.g., '/', '/users', etc.).
headers: A dictionary of HTTP headers.
body: The request body (as bytes).
```

The dispatch function should return a dictionary that contains the following keys:

```
status: The HTTP status code and reason phrase (e.g., '200 OK', '404 Not Found', etc.).
headers: A dictionary of HTTP headers.
body: The response body (as bytes).
```

## Testing

To test the server, you can use a tool like curl. For example:

```
$ curl http://localhost:8080/
Hello, World!
```

## License

This code is released under the GPL3 License. See LICENSE for more information.
