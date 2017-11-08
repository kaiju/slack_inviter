"""
Flask app to serve an invite page & provde an ajax endpoint to invite people to slack

This app relies on the SLACK_CHANNEL and SLACK_TOKEN environment variables for configuration.

SLACK_CHANNEL: Channel ID to invite people to
SLACK_TOKEN: Your Slack API access token

"""
from flask import Flask, request, render_template
import json
import requests
import os

app = Flask(__name__)

@app.route("/")
def page():
    return render_template('invite.html')

@app.route("/invite", methods=["POST"])
def invite():
    email = request.form['email']

    try:
        r = requests.post('https://slack.com/api/users.admin.invite', data={
            'email': email,
            'channels': os.environ['SLACK_CHANNEL'],
            'token': os.environ['SLACK_TOKEN'],
            'first_name': 'what',
            'last_name': 'who'
            })
    except requests.exceptions.ConnectionError:
        return (json.dumps({'ok': False, 'error': 'api_connection_error'}), 502, {'Content-type': 'application/json'})

    # just proxy the slack API response back to the client
    return (r.text, r.status_code, {'content-type': r.headers['Content-Type']})
