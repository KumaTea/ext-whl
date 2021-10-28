import os
from flask import Flask, send_from_directory
from urllib.parse import quote_plus


whl_dir = 'whl'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():
    html_code = ''
    whl_files = os.listdir(whl_dir)
    for whl_file in whl_files:
        html_code += f'<a href="{whl_dir}/{whl_file}">{quote_plus(whl_file)}</a><br>'
    return html_code, 200


@app.route('/whl/<path:path>', methods=['GET'])
def send_whl(path):
    return send_from_directory(whl_dir, path)


# If run on local machine:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10378, debug=False)
