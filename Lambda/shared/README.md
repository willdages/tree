The `tree.py` and `conditions.py` files contain classes that are used by multiple Lambda functions. They rely on being included with each package before upload to AWS Lambda. You will need to have the packages defined in `requirements.txt` installed in order to run the tests.

As shown in the `config-sample.yml` file, their inclusion can be automated when using the pylambdaws module, but for now you should manually include them in your zipped package for any Lambda functions that need to import `tree` or `conditions`.
