from __future__ import print_function
import boto3
import requests
import tinycss2
from tinycss2 import color3
import json
import keen
from tree import Tree
from conditions import Conditions


def handler(event, context):
  print(json.dumps(event))

  keen.project_id = event['keen_project_id']
  keen.write_key = event['keen_write_key']

  keen.add_event('speech', {
    'body': event['body'],
    'deviceId': event['device_id']
  })

  tree = Tree(event)
  c = Conditions(tree)

  sms = event['body'].lower()
  response = c.process(sms)

  if response is not 200:
      return response

  return
