# -*- encoding: utf-8 -*-
#
"""
First, install the latest release of Python wrapper: $ pip install ovh
"""
import json
import os  # pour récupérer les variables d'env
import re  # import regex

import ovh  # export ovh api
from decouple import config

# if service expired, you need to exclude them.
exclude_domains = ["bimscreen.fr"]

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
    endpoint=config("OVH_ENDPOINT"),
    application_key=config("OVH_APPLICATION_KEY"),
    application_secret=config("OVH_APPLICATION_SECRET"),
    consumer_key=config("OVH_CONSUMER_KEY"),
)

# print headers
print('"domain";"subdomain";"type";"record"')

# Print dns zone for each domain

domains = client.get("/domain/zone/")
for domain in domains:
    if domain not in exclude_domains:
        details = client.get("/domain/zone/%s/export" % domain)
        detailssansovh = re.sub(".*.ovh.net.*", "", details)
        regex1 = ".*IN.A.*"
        regex2 = ".*IN.CNAME.*"
        regexList = [regex1, regex2]

        for regex in regexList:
            filtereddetails = re.findall(regex, detailssansovh)
            for finding in filtereddetails:
                tmp = finding.split()

                # cas sous domaine vide
                if tmp[0] == "IN":
                    tmp.insert(0, "")

                # remove 'IN'
                tmp.remove("IN")

                # add domain
                tmp.insert(0, domain)

                for i, elem in enumerate(tmp):
                    print('"' + elem + '"', end="")
                    if i != len(tmp) - 1:
                        print(";", end="")
                print()
