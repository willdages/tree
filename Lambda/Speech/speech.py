from __future__ import print_function
import boto3
import requests
import tinycss2
from tinycss2 import color3
import json
import keen


def lambda_handler(event, context):
  print(json.dumps(event))

  global EVENT
  EVENT = event

  keen.project_id = event['keen_project_id']
  keen.write_key = event['keen_write_key']

  keen.add_event('speech', {
    'body': event['body'],
    'deviceId': event['device_id']
  })

  body = event['body']
  sms = body.lower()

  if body is None:
    return

  if sms in ['off', 'turn off']:
    set_color('[000,000,000]')

  if sms in ['on', 'turn on']:
    set_color('[255,255,255]')

  colors = [sms]
  separators = ['/', ' and ', ', ', ',', '+']
  for index, separator in enumerate(separators):
    # Check for multiple colors
    if len(colors) == 1:
      colors = sms.split(separator)
    else:
      alternate_colors(colors)

  if len(sms.split()) == 1:
    # Only 1 word sent
    rgba = tinycss2.color3.parse_color(sms)

    if rgba is not None and len(rgba) == 4:
      rgb_string = make_color_string(rgba)
      set_color(rgb_string)
    else:
      print(rgba)
      return 'Unknown color.'


def update_tree(fn, data):
  payload = {'access_token': EVENT['access_token'], 'command': data}
  try:
    r = requests.post("https://api.particle.io/v1/devices/{0}/{1}".format(EVENT['device_id'], fn), data=payload, timeout=7.0)
    print('Particle request status code: {}'.format(r.status_code))
    return
  except requests.exceptions.Timeout:
    print('Particle timeout')
    return 'Sorry, I can\'t contact the tree. It may be unplugged at the moment. Please try again later.'
  except requests.exceptions.RequestException:
    print('Particle exception')
    return 'Something unknown, unexpected, and possibly magical went wrong. Sorry, but I can\'t change the tree\'s color right now.'


def make_color_string(rgba):
    red = int(round(255*rgba[0]))
    green = int(round(255*rgba[1]))
    blue = int(round(255*rgba[2]))
    rgb_string = '[{0:03d},{1:03d},{2:03d}]'.format(red, green, blue)
    return rgb_string


def set_color(rgb_string):
  update_tree('wipe', rgb_string)


def rainbow(loop):
  update_tree('rainbow', loop)


def alternate_colors(colors):
  print('Alternating {0} colors'.format(len(colors)))
  for index, color in enumerate(colors):
    # For each color defined
    print(color)
    rgba = tinycss2.color3.parse_color(color)
    if len(rgba) == 4:
      rgb_string = make_color_string(rgba)
      for led in xrange(index, 25, len(colors)):
        # If 2 colors defined, set every other LED to this color.
        # If 3 colors defined, set every third LED to this color. ...etc
        print('{0}: {1}'.format(led, rgb_string))
        pixel_to_color(led, rgb_string)
    else:
        return 'Sorry, I don\'t recognize {} as a color.'.format(color)


def pixel_to_color(pixel, rgb_string):
  p = '{0:02d}'.format(pixel)
  pixel_string = '{0},{1}'.format(p, rgb_string)
  update_tree('pixel', pixel_string)
