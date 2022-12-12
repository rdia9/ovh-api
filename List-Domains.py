# -*- encoding: utf-8 -*-
#

import json
import os  # pour récupérer les variables d'env

import ovh  # export ovh api
from decouple import config

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
    endpoint=config("OVH_ENDPOINT"),
    application_key=config("OVH_APPLICATION_KEY"),
    application_secret=config("OVH_APPLICATION_SECRET"),
    consumer_key=config("OVH_CONSUMER_KEY"),
)

# print headers
print('"domain"')

# Print dns zone for each domain
domains = client.get("/domain/zone/")
for i, elem in enumerate(domains):
    print('"' + elem + '"', end="")
    print()
