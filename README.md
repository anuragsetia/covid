# covid
Dashboards for COVID19 progress &amp; impact in India. Source: covid19india.org APIs

To run these python scripts, please install requirements as follows -

    pip install -r requirements.txt

Setup environment variable 'FLASK_APP' to main.py and then run it from the command line to generate the chart using flask -

    flask run

Once the application is running, each of the charts is published as an image therefore, an HTTP Get request can be used to generate the required charts which can be included in a webpage or document.

## Pre-requisities

1. Python v3 onwards
2. pip
