# An internet-connected holiday tree

Last year I built ['The Texting Tree'](http://willd.me/posts/the-texting-tree), and internet-connected holiday tree that responded to text messages by changing the color of its lights. The code for the original tree is here: [The-Texting-Tree on GitHub](https://github.com/willdages/The-Texting-Tree).

This year (2015), the project has been re-worked and expanded. I replaced the Heroku/Flask server piece with AWS API Gateway and AWS Lambda functions. A new tutorial is coming soon.

Some fun new features added to the tree this year:

* Custom text or gif responses to specific non-color text messages
* Analytics via Keen.io (reported on by phone call)
* Speech Recognition over the web via the Web Speech API
* A Slack slash command to control the tree

For setup/development/deployment instructions for each piece, please check the README in each directory.
