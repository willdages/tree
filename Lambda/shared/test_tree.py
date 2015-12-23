import unittest
from mock import MagicMock
from tinycss2 import color3
from tree import Tree


class TestStringMethods(unittest.TestCase):

  def test_init(self):
    event = {
        'text': 'blue'
    }
    tree = Tree(event)
    self.assertEqual(event, tree.event)


  def test_is_valid_rgb_string(self):
    tree = Tree({})
    validStrings = ['[255,255,255]',
                    '[000,000,000]',
                    '[128,128,128]']
    invalidStrings = ['[25,255,255]',
                      '[255255,255]',
                      '[255,2$5,255]',
                      '[2550,2550,2550',
                      '[255,OOO,255]',
                      '[255,255,2550]']

    for string in validStrings:
      result = tree.is_valid_rgb_string(string)
      self.assertTrue(result)

    for string in invalidStrings:
      result = tree.is_valid_rgb_string(string)
      self.assertFalse(result)


  def test_make_color_string(self):
    tree = Tree({})
    red = color3.parse_color('red')
    green = color3.parse_color('lime') # 'green' is not full green wtf
    blue = color3.parse_color('blue')
    self.assertEqual(tree.make_color_string(red), '[255,000,000]')
    self.assertEqual(tree.make_color_string(green), '[000,255,000]')
    self.assertEqual(tree.make_color_string(blue), '[000,000,255]')


  def test_set_color(self):
    tree = Tree({})
    tree.update = MagicMock()
    tree.set_color('[255,000,000]')
    tree.update.assert_called_with('wipe', '[255,000,000]')


  def test_set_color_with_keyword(self):
    tree = Tree({})

    # Set color with a valid keyword
    tree.set_color = MagicMock()
    tree.set_color_with_keyword('red')
    tree.set_color.assert_called_with('[255,000,000]')

    # Set color with an invalid keyword
    tree.set_color.reset_mock()
    tree.set_color_with_keyword('invalidKeyword')
    tree.set_color.assert_not_called()


  def test_rainbow(self):
    tree = Tree({})
    tree.update = MagicMock()
    tree.rainbow('1')
    tree.update.assert_called_with('rainbow', '1')


  def test_alternate(self):
    tree = Tree({})
    tree.update = MagicMock()
    tree.alternate(['blue', 'red'])
    tree.update.assert_called_once_with('alternate', '02,[000,000,255],[255,000,000]')


if __name__ == '__main__':
    unittest.main()
