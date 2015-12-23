from __future__ import print_function
import tinycss2
from tinycss2 import color3
import json
import keen
import requests
from tree import Tree
from conditions import Conditions


def handler(event, context):
  print(json.dumps(event))

  keen.project_id = event['keen_project_id']
  keen.write_key = event['keen_write_key']

  keen.add_event('slack', {
    'body': event['text'],
    'deviceId': event['device_id'],
    'team_domain': event['team_domain'],
    'channel_name': event['channel_name'],
    'user_name': event['user_name']
  })

  tree = Tree(event)
  c = Conditions(tree)

  sms = event['text'].lower()
  response = c.process(sms)

  if response is 200:
      message = { 'response_type': 'in_channel', 'text': '@{0} changed the tree to {1}!'.format(event['user_name'], sms) }
      r = requests.post(event['response_url'], data=json.dumps(message), headers=headers)
      print('Tree is now response code: {}'.format(r.status_code))
      print(r.text)
  else:
      message = { "response_type": "ephemeral", "text": response }
      r = requests.post(event['response_url'], data=json.dumps(message), headers=headers)
      print('Special message response code: {}'.format(r.status_code))
      print(r.text)

  return ''
