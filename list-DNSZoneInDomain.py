# -*- encoding: utf-8 -*-
#

import ovh

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint='ovh-eu',
	application_key='XXXXXXXXXXXXXXXXXXXXXXXX',
	application_secret='XXXXXXXXXXXXXXXXXXXXXXXXXX',
	consumer_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
)
# Print dns zone for each domain

domains = client.get('/domain/zone/')
for domain in domains:
    details = client.get('/domain/zone/%s/export' % domain)
    print ('--------------')
    print (domain)
    print ('--------------')
    print (details)


