from __future__ import print_function
import boto3
import requests
import tinycss2
from tinycss2 import color3
import json
import keen
import twilio.twiml
from twilio.rest import TwilioRestClient
from tree import Tree
from conditions import Conditions


def handler(event, context):
  print(json.dumps(event))

  keen.project_id = event['keen_project_id']
  keen.write_key = event['keen_write_key']

  keen.add_event('sms', {
    'body': event['body'],
    'fromNumber': event['fromNumber'],
    'toNumber': event['toNumber'],
    'deviceId': event['device_id'],
    'fromCity': event['fromCity'],
    'fromState': event['fromState'],
    'fromZip': event['fromZip']
  })

  tree = Tree(event)
  c = Conditions(tree)

  sms = event['body'].lower()
  response = c.process(sms)

  if response is not 200:
      client = TwilioRestClient(event['twilio_sid'], event['twilio_auth_token'])
      client.messages.create(from_=event['toNumber'], to=event['fromNumber'], body=response)

  return
