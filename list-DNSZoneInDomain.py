# -*- encoding: utf-8 -*-
#
'''
First, install the latest release of Python wrapper: $ pip install ovh
'''
import json
import ovh # export ovh api
import os # pour récupérer les variables d'env
import re # import regex

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint= os.environ['ovh_endpoint'] ,
	application_key= os.environ['ovh_application_key'] ,
	application_secret= os.environ['ovh_application_secret'] ,
	consumer_key= os.environ['ovh_consumer_key'] ,
)
# Print dns zone for each domain

domains = client.get('/domain/zone/')
for domain in domains:
    details = client.get('/domain/zone/%s/export' % domain)
    detailssansovh = re.sub('.*.ovh.net.*', '', details)
    regex1 = '.*IN.A.*'
    regex2 = '.*IN.CNAME.*'
    regexList = [regex1, regex2]

    print('"domain";"subdomain";"type";"record"')

    for regex in regexList:
        filtereddetails = re.findall(regex, detailssansovh)
        for finding in filtereddetails:
            tmp = finding.split()

            # cas sous domaine vide
            if(tmp[0]=='IN'):
                tmp.insert(0,'')

            # remove 'IN'
            tmp.remove('IN')

            # add domain
            tmp.insert(0, domain)

            for i, elem in enumerate(tmp):
                print('"' + elem + '"', end='')
                if(i != len(tmp)-1):
                    print(';', end='')
            print()