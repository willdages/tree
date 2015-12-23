Lambda functions
---

These directories each include a Lambda function. They use [Virtualenv](https://virtualenv.readthedocs.org/en/latest/) for managing dependencies. These are designed to reside behind an AWS API Gateway distribution with specific mapping templates and Staging variables.

### Requirements

* Python 2.7
* [Virtualenv](https://virtualenv.readthedocs.org/en/latest/)

## Development

Set up your virtual environment and install dependencies:

    $ cd ProjectDirectory
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements/prod.txt

### Packaging

Prepare the package for upload:

    $ cd FunctionDirectory
    $ zip -9 package.zip filename.py
    $ zip -9 package.zip ../shared/tree.py # optional, if needed
    $ cd venv/lib/python2.7/site-packages
    $ zip -r9 ~/path/to/package.zip *

Upload `package.zip` through the AWS Lambda console.
