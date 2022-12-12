# -*- encoding: utf-8 -*-
#

import json
import os  # pour récupérer les variables d'env

import ovh  # export ovh api
from decouple import config

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
    endpoint=config("ovh_endpoint"),
    application_key=config("ovh_application_key"),
    application_secret=config("ovh_application_secret"),
    consumer_key=config("ovh_consumer_key"),
)

# print headers
print('"domain"')

# Print dns zone for each domain
domains = client.get("/domain/zone/")
for i, elem in enumerate(domains):
    print('"' + elem + '"', end="")
    print()
