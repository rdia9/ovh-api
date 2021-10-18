# -*- encoding: utf-8 -*-
#
'''
First, install the latest release of Python wrapper: $ pip install ovh
'''
import json
import ovh # export ovh api
import re # import regex

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint= "${{ ovh_endpoint }}" ,
	application_key= "${{ ovh_application_key }}" ,
	application_secret= "${{ ovh_application_secret }}" ,
	consumer_key= "${{ ovh_consumer_key }}" ,
)
# Print dns zone for each domain

domains = client.get('/domain/zone/')
for domain in domains:
    details = client.get('/domain/zone/%s/export' % domain)
    detailssansovh = re.sub('.*.ovh.net.*', '', details)
    regex1='.*IN.A.*'
    regex2='.*IN.CNAME.*'
    regexList = [regex1, regex2]
    for regex in regexList:
        filtereddetails = re.findall(regex, detailssansovh)
        print ('--------------') # to remove to have correct json
        print (domain)           # to remove to have correct json
        print ('--------------') # to remove to have correct json
        print(json.dumps(filtereddetails, indent=4))


