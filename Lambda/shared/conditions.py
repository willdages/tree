from __future__ import print_function

class Conditions:

    def __init__(self, tree):
        self.tree = tree


    def process(self, command):

        is_special = self.is_special_keyword(command)
        if is_special is not False:
            print('Special keyword detected')
            return is_special

        multiple_colors = self.has_multiple(command)
        if multiple_colors is not False:
            print('Multiple colors detected')
            return self.tree.alternate(multiple_colors)

        if len(command.split()) == 1:
            # Only 1 word sent
            print('Single color detected')
            return self.tree.set_color_with_keyword(command)
        else:
            print('No matches')
            return 'Huh?'


    def has_multiple(self, command):
        colors = [command]
        separators = [' / ', '/', ' & ', '&', ' and ', ', ', ',', ' + ', '+']
        for separator in separators:
          # Check for multiple colors
          if len(colors) == 1:
            # Still just 1, try splitting with another separator
            colors = command.split(separator)
          else:
            return colors

        return False


    def is_special_keyword(self, command):

        if command in ['?', 'what', 'what?', 'huh?', 'explain', 'directions', \
                  'instructions', 'how does this work', 'how does this work?']:
          return u"\U0001F385 Merry Christmas! Text me a color to change the \U0001F384."


        if u'\U0001F385' in command:
          # Reverse the lookup because different skin tones come in as multiple unicode characters,
          # one for the emoji and one for the color overlay
          return 'SSSAAAAANTTTTAAAAAA!!!!!! I KNOW HIM!!!\n\nI know him.\n\nhttps://youtu.be/B3FSFXJmdp8'


        if u'\U0001F384' in command:
          # The Christmas Tree Emoji
          return 'http://i.imgur.com/Dmg0RH9.gif'


        if command in [u"\u2603", u"\u26C4"]:
          # The Snowman Emoji
          return u"\U0001F3b6 Do you wanna build a snowman? \U0001F3b6"


        if u'\U0001F4A9' in command:
          # Poop emoji
          return 'https://youtu.be/TMVEK4WvzqE'


        if u'\U0001F381' in command:
          # Gift emoji
          return 'For me? Aww, you shouldn\'t have. Ok ok, I got you something too. "It\'s the gift that keeps on giving the whooole year."\n\nhttps://youtu.be/TQXuazYI_YU?t=27s'


        if u'\u2615' in command:
          # Coffee emoji
          return 'http://i.giphy.com/nrVixVKLQ8Cyc.gif'


        if u'\U0001F308' in command:
          # Rainbow emoji
          self.tree.rainbow('1')
          return 'You have unlocked an epic achievement.'


        if command in ['merry christmas', 'merry xmas', 'merry christmas!']:
          self.tree.rainbow('0')
          return u'\U0001F385 Merry Christmas to you, too!'


        if command in ['off', 'turn off']:
          self.tree.set_color_with_keyword('black')
          return u'Oh... ok. \U0001F61E'


        if command in ['on', 'turn on']:
          self.tree.set_color_with_keyword('white')
          return u'\U0001F384'


        if command in ['transparent']:
          return u"\U0001F47B"


        if command in ['fire', 'forest fire', 'catch on fire', 'light on fire']:
          self.tree.alternate(['red', 'orange', 'yellow'])
          return u'\U0001F692 You monster. \U0001F525'

        return False
