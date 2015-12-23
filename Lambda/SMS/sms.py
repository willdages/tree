from __future__ import print_function
import boto3
import requests
import tinycss2
from tinycss2 import color3
import json
import keen
import twilio.twiml
from twilio.rest import TwilioRestClient


def lambda_handler(event, context):
  print(json.dumps(event))

  global EVENT
  EVENT = event

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

  body = event['body']
  sms = body.lower()

  if body is None:
    return

  if sms in ['?', 'what', 'what?', 'huh?', 'explain', 'directions', \
            'instructions', 'how does this work', 'how does this work?']:
    send_message(u"\U0001F385 Merry Christmas! Text a color to change the \U0001F384.")
    return

  if u'\U0001F385' in sms:
    # Reverse the lookup because different skin tones come in as multiple unicode characters,
    # one for the emoji and one for the color overlay
    send_message('SSSAAAAANTTTTAAAAAA!!!!!! I KNOW HIM!!!\n\nI know him.\n\nhttps://youtu.be/B3FSFXJmdp8')
    return

  if u'\U0001F384' in sms:
    # The Christmas Tree Emoji
    send_img('http://i.imgur.com/Dmg0RH9.gif')
    return

  if sms in [u"\u2603", u"\u26C4"]:
    # The Snowman Emoji
    send_message(u"\U0001F3b6 Do you wanna build a snowman? \U0001F3b6")
    return

  if u'\U0001F4A9' in sms:
    # Poop emoji
    send_message('https://youtu.be/TMVEK4WvzqE')
    return

  if u'\U0001F381' in sms:
    # Gift emoji
    send_message('For me? Aww, you shouldn\'t have. Ok ok, I got you something too. "It\'s the gift that keeps on giving the whooole year."\n\nhttps://youtu.be/TQXuazYI_YU?t=27s')
    return

  if u'\u2615' in sms:
    # Coffee emoji
    send_img('http://i.giphy.com/nrVixVKLQ8Cyc.gif')
    return

  if u'\U0001F308' in sms:
    # Rainbow emoji
    rainbow('1')
    return


  if sms in ['merry christmas', 'merry xmas', 'merry christmas!']:
    send_message(u"\U0001F385 Merry Christmas to you, too!")
    rainbow('0')
    return

  if sms in ['off', 'turn off']:
    send_message(u"Oh... ok. \U0001F61E")
    set_color('[000,000,000]')
    return

  if sms in ['on', 'turn on']:
    send_message(u"\U0001F384")
    set_color('[255,255,255]')
    return

  if sms in ['transparent']:
    send_message(u"\U0001F47B")
    return

  if sms in ['fire', 'forest fire', 'catch on fire', 'light on fire']:
    send_message(u"\U0001F692 You monster. \U0001F525")
    sms = 'red and orange and yellow'

  colors = [sms]
  separators = ['/', ' and ', ', ', ',', '+']
  for index, separator in enumerate(separators):
    # Check for multiple colors
    if len(colors) == 1:
      colors = sms.split(separator)
    else:
      alternate_colors(colors)
      return

  if len(sms.split()) == 1:
    # Only 1 word sent
    rgba = tinycss2.color3.parse_color(sms)

    if rgba is not None and len(rgba) == 4:
      rgb_string = make_color_string(rgba)
      #send_message(u"Look! The tree is turning {}".format(sms))
      set_color(rgb_string)
      return
    else:
      send_message('Sorry, I couldn\'t make sense of that color. Try something simpler? I\'m only a tree, you know.')
      return
  else:
      return


def send_message(body):
  client = TwilioRestClient(EVENT['twilio_sid'], EVENT['twilio_auth_token'])
  client.messages.create(from_=EVENT['toNumber'], to=EVENT['fromNumber'], body=body)


def send_img(url):
  client = TwilioRestClient(EVENT['twilio_sid'], EVENT['twilio_auth_token'])
  client.messages.create(from_=EVENT['toNumber'], to=EVENT['fromNumber'], media_url=url)


def update_tree(fn, data):
  payload = {'access_token': EVENT['access_token'], 'command': data}
  try:
    r = requests.post("https://api.particle.io/v1/devices/{0}/{1}".format(EVENT['device_id'], fn), data=payload, timeout=7.0)
    print('Particle request status code: {}'.format(r.status_code))
    return
  except requests.exceptions.Timeout:
    print('Particle timeout')
    send_message('Sorry, I can\'t contact the tree. It may be unplugged at the moment. Please try again later.')
    return
  except requests.exceptions.RequestException:
    print('Particle exception')
    send_message('Something unknown, unexpected, and possibly magical went wrong. Sorry, but I can\'t change the tree\'s color right now.')
    return


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
      if index == 0:
        # Save on requests by starting with a wipe, and then cherry-picking the rest
        set_color(rgb_string)
      else:
        for led in xrange(index, 25, len(colors)):
          # If 2 colors defined, set every other LED to this color.
          # If 3 colors defined, set every third LED to this color. ...etc
          print('{0}: {1}'.format(led, rgb_string))
          pixel_to_color(led, rgb_string)
    else:
      send_message('Sorry, I don\'t recognize {} as a color.'.format(color))
      return


def pixel_to_color(pixel, rgb_string):
  p = '{0:02d}'.format(pixel)
  pixel_string = '{0},{1}'.format(p, rgb_string)
  update_tree('pixel', pixel_string)
