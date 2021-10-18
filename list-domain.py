# -*- encoding: utf-8 -*-
#

import ovh

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint="${{ secrets.ENDPOINT }}",
	application_key="${{ secrets.APPLICATION_KEY }}",
	application_secret="${{ secrets.APPLICATION_SECRET }}",
	consumer_key="${{ secrets.CONSUMER_KEY }}",
)
# Print every domain you have
print("Welcome", client.get('/domain/zone/'))
