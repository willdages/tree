from __future__ import print_function
import re
import requests
from tinycss2 import color3

class Tree:

    def __init__(self, event):
        self.event = event


    def is_valid_rgb_string(self, string):
        match = re.search('\A\[(\d{3}\,{1}){2}(\d{3})[\]]', string)
        return True if match is not None else False


    def set_color_with_keyword(self, keyword):
        rgba = color3.parse_color(keyword)
        if rgba is not None:
            rgb_string = self.make_color_string(rgba)
            return self.set_color(rgb_string)
        else:
            return 'Sorry, I don\'t recognize {0} as a color. I\'m only a tree, not the Google'.format(keyword)


    def set_color(self, rgb_string):
        return self.update('wipe', rgb_string)


    def rainbow(self, loop):
        return self.update('rainbow', loop)


    def pixel_to_color(self, pixel, rgb_string):
        p = '{0:02d}'.format(pixel)
        pixel_string = '{0},{1}'.format(p, rgb_string)
        return self.update('pixel', pixel_string)


    def make_color_string(self, rgba):
        strings = ['{0:03d}'.format(int(round(255*color))) for color in rgba]
        rgb_string = '[{0},{1},{2}]'.format(strings[0], strings[1], strings[2])
        if self.is_valid_rgb_string(rgb_string):
            return rgb_string
        else:
            return None


    def alternate(self, colors):
        for index, color in enumerate(colors):
            rgba = color3.parse_color(color)
            if rgba is None:
                return 'Sorry, I don\'t recognize {} as a color. I\'m only a tree, not the Google'.format(color)

            rgb_string = self.make_color_string(rgba)
            if index == 0:
                # Save on requests by starting with a wipe, and then cherry-picking the rest
                self.set_color(rgb_string)
            else:
                for led in xrange(index, 25, len(colors)):
                    # If 2 colors defined, set every other LED to this color.
                    # If 3 colors defined, set every third LED to this color. ...etc
                    response = self.pixel_to_color(led, rgb_string)
                    if response is not 200:
                        break

        return 200


    def update(self, fn, data):
        payload = {'access_token': self.event['access_token'], 'command': data}
        try:
            r = requests.post("https://api.particle.io/v1/devices/{0}/{1}".format(self.event['device_id'], fn), data=payload, timeout=7.0)
            print('Particle request status code: {}'.format(r.status_code))
            return 200
        except requests.exceptions.Timeout:
            print('Particle timeout')
            return 'Sorry, I can\'t contact the tree. It may be unplugged at the moment. Please try again later.'
        except requests.exceptions.RequestException:
            print('Particle exception')
            return 'Something unknown, unexpected, and possibly magical went wrong. Sorry, but I can\'t change the tree\'s color right now.'
