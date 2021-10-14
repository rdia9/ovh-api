# -*- encoding: utf-8 -*-
#

import ovh

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint='ovh-eu',
	application_key='XXXXXXXXXXXXXXXXXXXXXXX',
	application_secret='XXXXXXXXXXXXXXXXXXXXXXX',
	consumer_key='XXXXXXXXXXXXXXXXXXXXXXX',
)
# Print every domain you have
print(client.get('/domain/zone/'))
