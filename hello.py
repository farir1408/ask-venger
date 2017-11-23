from pprint import pformat
from urllib import parse

def application(environ, start_response):
    output = [b'<!DOCTYPE html>', b'<html>', b'<p>WSGI</p>']

    output.append(b'Post:')
    output.append(b'<form method="post">')
    output.append(b'<input type="text" name="test">')
    output.append(b'<input type="submit" value="Send">')
    output.append(b'</form>')

    d = parse.parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        output.append(b'<h1>Post data:</h1>')
        output.append(pformat(environ['wsgi.input'].read()).encode('u8'))

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            output.append(b'<h1>Get data:</h1>')
            for ch in d:
                output.append((' = '.join(ch)).encode('u8'))
                output.append(b'<br>')

    output.append(b'</html>')

    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])

    return output