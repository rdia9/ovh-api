# -*- encoding: utf-8 -*-
#

import ovh # export ovh api
import os # pour récupérer les variables d'env

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# # to get your credentials
client = ovh.Client(
	endpoint= os.environ['ovh_endpoint'] ,
	application_key= os.environ['ovh_application_key'] ,
	application_secret= os.environ['ovh_application_secret'] ,
	consumer_key= os.environ['ovh_consumer_key'] ,
)
# Print every domain you have
print(client.get('/domain/zone/'))
