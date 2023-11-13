#!/usr/bin/env python3
"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Hyeyoung Kim <hyeyokim@cisco.com>", "Lakshya Tyagi <ltyagi@cisco.com>"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import urllib3
import json
import os
import time

from flask import Flask,request, abort
from flask_basicauth import BasicAuth
from dotenv import load_dotenv
import pymsteams

#Load the env file
project_folder = os.path.expanduser('./')

load_dotenv(os.path.join(project_folder,'.env'))
 
#Authentication Information
WEBHOOK_USERNAME = str(os.getenv("WEBHOOK_USERNAME"))
WEBHOOK_PASSWORD = str(os.getenv("WEBHOOK_PASSWORD"))
MSTEAMS_URL = str(os.getenv("MSTEAMS_URL"))

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = WEBHOOK_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = WEBHOOK_PASSWORD

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def index():
    return '<h1>Flask Webhook Test page </h1>', 200


@app.route('/', methods = ['POST'])
@basic_auth.required
def webhook():
    if request.method == "POST":
        title = "DNAC Notification"
        content = request.json

        message = pymsteams.connectorcard(MSTEAMS_URL)
        message.title(title)
        

        message_detail_section = pymsteams.cardsection()
        #message_detail_section.text("Notification Details")

        for (v,k) in content.items():
            message_detail_section.addFact(str(v), str(k))

        message.addSection(message_detail_section)


        message_raw_section = pymsteams.cardsection()
        #message_raw_section.text("Raw data")
        message_raw_section.addFact("raw data : ", str(content))

        message.addSection(message_raw_section) 
        message.summary("summary")
        message.send()

        return 'Webhook notification received', 202
    else:
        return 'POST Method not support', 405


if __name__ == '__main__':
    app.run(port=5443, ssl_context='adhoc', debug=True)


        
