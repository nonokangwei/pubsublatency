# Copyright 2021 Google. This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.

from google.cloud import bigquery
import json

# Read events data from a local file called local_file.json
with open('items.json', 'r') as json_file:
    data = json.load(json_file)

print(data)