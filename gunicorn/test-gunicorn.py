import json

bind = "127.0.0.1:8081"


def app(environ, start_response):
    data = f" \
        REQUEST_METHOD: {environ['REQUEST_METHOD']}\n \
        RAW_URI': {environ['RAW_URI']}\n \
        CONTENT_TYPE': {environ['CONTENT_TYPE']}\n \
        CONTENT_LENGTH': {environ['CONTENT_LENGTH']}\n \
        wsgi.input': {environ['wsgi.input'].read()}\n \
    "
    print('---- Begin ----')
    print(data)
    print('---- End ----\n\n')

    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data))),
    ]
    start_response(status, response_headers)

    return iter([b'OK\n'])
