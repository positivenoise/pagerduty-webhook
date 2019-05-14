# Webhook.py: Webhook listener for PagerDuty custom events
# Reads authentication from default boto3 config - use "aws configure" to setup
#
# -*- coding: utf-8 -*-

import os
import boto3
import requests
import pypd

from flask import Flask, request, abort

app = Flask(__name__)
pypd.api_key = os.environ['PAGERDUTY_API_KEY']
from_email = os.environ['FROM_EMAIL_ADDRESS']


@app.before_request
def limit_pagerduty_ips():
    """Ensures request is coming from PagerDuty"""
    allowedips = requests.get('https://app.pagerduty.com/webhook_ips')
    if request.remote_addr not in allowedips.text:
        abort(403)


def ec2_terminate(id):
    """Terminates a given ec2 instance by ID"""
    ec2 = boto3.client('ec2')
    return ec2.terminate_instances(
        InstanceIds=[id]
    )


@app.route('/terminate', methods=['POST'])
def terminate():
    """Webhook receiver for terminate function"""
    if request.method == 'POST':
        incident_summary = request.json['messages'][0]['incident']['description']
        incident_id = request.json['messages'][0]['incident']['incident_number']
        incident = pypd.Incident.fetch(id=str(incident_id))
        
        for id in incident_summary.split(" "):
            if id.startswith("i-"):
                try:
                    print(incident.create_note(from_email, str(ec2_terminate(id))))
                    print(incident.resolve(from_email, "Resolved OK"))
                except:
                    print("Error resolving incident")
        return '', 200
    else:
        abort(400)
