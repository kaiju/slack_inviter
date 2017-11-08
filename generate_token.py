#!/usr/bin/env python
"""
Quick & dirty utility to help obtain a slack api token w/ 'client'
scope.

This script gives you an OAuth authorization URL and also provides
an OAuth redirect endpoint which will request an OAuth access token
using the given code.

You will need to create a new Slack application via https://api.slack.com/
belonging to your Slack workspace.

Grab the Client ID and Client Secret values from that application for use
in this script.

Be sure to set the OAuth redirect url to http://localhost:(configured port).

Author: Josh <josh@kaiju.net>
"""

import requests
import os
import http.server
import urllib.parse

PORT = 8080             # Port to run OAuth redirect endpoint on
WORKSPACE_URL = ''      # your workspace url (ex: https://my-workspace.slack.com)
CLIENT_ID = ''          # your slack app client id
CLIENT_SECRET = ''      # your slack app client secret

class OAuthEndpointServer(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def do_GET(self):
        request_parts = urllib.parse.urlparse(self.path)

        if request_parts.path == '/':
            # Grab 'code' parameter out of the request
            params = urllib.parse.parse_qs(request_parts.query)
            code = params.get('code')[0]

            # Make a oauth.access request to the slack.api to get our API access token
            request_args = {
                'workspace_url': WORKSPACE_URL,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code
            }

            r = requests.get('{workspace_url}/api/oauth.access?client_id={client_id}&client_secret={client_secret}&code={code}'.format(**request_args))

            slack_response = r.json()

            # Send output to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if 'access_token' in slack_response:
                self.wfile.write(bytes('Your access token is: <b>{}</b>'.format(slack_response['access_token']), 'utf-8'))
                print()
                print('Your slack API access token is: {}'.format(slack_response['access_token']))
                print()
            else:
                self.wfile.write(bytes('Got a bad response from Slack: <b>{}</b>'.format(slack_response), 'utf-8'))
                print()
                print('Got a bad response from Slack: {}'.format(slack_response))
                print()

print('Starting OAuth Endpoint on port {}...'.format(PORT))
print('Make sure your Slack application\'s OAuth redirect is set to http://localhost:{}'.format(PORT))
print()
print('Open {workspace_url}/oauth/authorize?client_id={client_id}&scope=client in your favorite browser'.format(workspace_url=WORKSPACE_URL, client_id=CLIENT_ID))
httpd = http.server.HTTPServer(('', PORT), OAuthEndpointServer)
httpd.handle_request()
