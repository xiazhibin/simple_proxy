from contextlib import closing

from flask import Flask, request, Response
import requests

app = Flask(__name__)


@app.before_request
def before_request():
    url = request.url
    method = request.method
    data = request.get_data()
    headers = dict()
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value
    print 'url:%s' % url
    with closing(
            requests.request(method, url, headers=headers, data=data, stream=True)
    ) as r:
        response_headers = []
        for name, value in r.headers.items():
            if name.lower() in ('content-length', 'connection', 'content-encoding'):
                continue
                response_headers.append((name, value))
        return Response(r.content, status=r.status_code, headers=response_headers)


if __name__ == '__main__':
    app.run()
