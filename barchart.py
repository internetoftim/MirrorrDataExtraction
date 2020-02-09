# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
import barchart_extraction
from barchart_extraction import *
import jsonify
# import importlibe
# from importlib.machinery import SourceFileLoader
from flask import request



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return "'<h1>Barchart Scraping Demo</h1>"

@app.route('/url')
def userid_landing():
    return "Barchart Scraping Demo: enter /url/<company>"

@app.route('/url/<string:url>', methods=['GET'])
def extract_url(url):
#     user=InstaUser(userid=name)
#     user.quick_demo()
#     out_html = user.get_info() + "<div><img src="+ user.profile_pic_uri+"></div>" 

#     return out_html
    extract_barchart_site(write_option='a',name=url)
    return "'<h1>Extraction was initiated. Saving to file: " + url + ".csv<\h1>'"

@app.route('/extract')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    try:
        code = request.args.get('code')
        filename = request.args.get('file')
        print('code is: ' + code)
        print('filename is: ' + filename)
        extract_barchart_code(input_code=code,write_option='a',name=filename)
        return "<h1>Extraction was initiated on code " + code + " . Saving to file: " + filename + ".csv<\h1>"

    except:
        out = "Barchart Scraping Demo: enter /extract?code=<company>"
        
    try:
        input_url = request.args.get('url')
        filename = request.args.get('file')        
        print('url is: ' + input_url)
        print('filename is: ' + filename)
        
        extract_barchart_site(input_url=input_url,write_option='a',name=filename)
        return "<h1>Extraction was initiated on url " + input_url + " . Saving to file: " + filename + ".csv<\h1>"

    except:
        out = "Barchart Scraping Demo: enter /extract?code=<company>"
        
    return out

@app.route('/code/<string:code>', methods=['GET'])
def extract_code(code):
#     user=InstaUser(userid=name)
#     user.quick_demo()
#     out_html = user.get_info() + "<div><img src="+ user.profile_pic_uri+"></div>" 

#     return out_html
    extract_barchart_site_code(input_code=code,write_option='a',name='tests')
    return "'<h1>Extraction was initiated on code " + code + " . Saving to file: " + url + ".csv<\h1>'"



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
