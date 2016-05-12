#!/bin/sh

pip install coveralls
pip install coverage
pip install --extra-index-url https://pypi.fury.io/$GEMFURY_KEY/silver-saas/ thriftplus
pip install --extra-index-url "https://pypi.fury.io/$GEMFURY_KEY/silver-saas/" -r requirements.txt
