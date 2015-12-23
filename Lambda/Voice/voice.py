from __future__ import print_function
import boto3
import keen
import json
import emoji

def lambda_handler(event, context):
  print(json.dumps(event))

  # A filter for Keen to only return stats for this device
  this_device_filter = [{'property_name':'deviceId', 'operator':'eq', 'property_value':event['device_id']}]

  keen.project_id = event['keen_project_id']
  keen.read_key = event['keen_read_key']
  keen.write_key = event['keen_write_key']

  keen.add_event('call', {
    'fromNumber': event['from'],
    'toNumber': event['to'],
    'deviceId': event['device_id']
  })

  changes = keen.count('sms', timeframe='today', timezone='US/Eastern', filters=this_device_filter)
  people = keen.count_unique('sms', target_property='fromNumber', timeframe='today', timezone='US/Eastern', filters=this_device_filter)

  response = "Hello! I've changed colors {0} times today, thanks to messages from {1} different people. Merry Christmas!".format(changes, people)
  return response
