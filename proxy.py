from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return '''
    <h2>🛰️ YouTube Proxy is Running!</h2>
    <p>Use like this:</p>
    <code>/www.youtube.com</code><br><br>
    <b>Example:</b><br>
    <a href="/www.youtube.com">/www.youtube.com</a>
    '''

@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    target_url = f'https://{path}'
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key.lower() != 'host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            stream=True
        )

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f'Proxy Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
