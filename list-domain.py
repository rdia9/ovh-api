# -*- encoding: utf-8 -*-
#

import ovh

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint= "${{ ovh_endpoint }}" ,
	application_key= "${{ ovh_application_key }}" ,
	application_secret= "${{ ovh_application_secret }}" ,
	consumer_key= "${{ ovh_consumer_key }}" ,
)
# Print every domain you have
print("Welcome", client.get('/domain/zone/'))
