#!/usr/bin/python3

import os
import ovh
import requests
import json
import sys

# Get our current IP address as we will need it to restrict our rigths later
my_IP = requests.get("https://ifconfig.me").text


# create a client using configuration
client = ovh.Client(
    endpoint=str(os.getenv('OVH_ENDPOINT')),               # Endpoint of API OVH Europe
    application_key=str(os.getenv('OVH_APPLICATION_KEY')), # Lootibox (TO DO : change for a more appropriate app)
    application_secret=str(os.getenv('OVH_APPLICATION_SECRET')) # TO DO : change accortingly to the new application chosen
)

# Request RO, /me API access
ck = client.new_consumer_key_request()
ck.add_rule("GET", f"/BTPrestrictedIP/{my_IP}")
ck.add_rules(ovh.API_READ_ONLY, "/me")
ck.add_recursive_rules(["GET", "PUT", "DELETE"], '/me/api/credential/*') # Needed to clean expired credentials and restrict IP
ck.add_recursive_rules(ovh.API_READ_WRITE, '/domain/zone/*')

# Request token
validation = ck.request(allowedIPs=[f"{my_IP}/32"])

#sys.exit(-1)

print("Please visit this URL to authenticate:")
print(validation['validationUrl'])
input("And press Enter to continue...")

# Print nice welcome message
ovh_user = client.get('/me')
print(f"Welcome, {ovh_user['firstname']}'s padawan !")

# Lets limit our access to the current IP adress !
print(f"We will restrict the credentials access to {my_IP}/32")

# Cleaning
print("Lets also clean up your old and expired credentials...")
for credential_id in client.get('/me/api/credential'):
    credential = client.get(f'/me/api/credential/{credential_id}')
    #print(json.dumps(credential, indent=4))
    # ApplicationId hardcoded to add safety during the build, but should be removed after
    if credential['applicationId'] == 204612:
        # Delete expired credentials
        if credential['status'] == "expired":
            client.delete(f'/me/api/credential/{credential_id}')
            print(f"Credential with ID={credential_id} deleted")
        # Add IP restriction to our credential if found
        if {"method": "GET","path": f"/BTPrestrictedIP/{my_IP}"} in credential['rules'] and credential['status'] != "expired":
            print(f"Found credential with ID={credential_id} to be restricted")
            response = client.put(f'/me/api/credential/{credential_id}', allowedIPs=[f'{my_IP}/32'])

print("Please find bellow your OVH credentials.")
print("You should export them to your Bash env, as these values (especially the 'consumerKey') are not recorded anywhere else.")
print(f"export OVH_ENDPOINT={str('ovh-eu')}")
print(f"export OVH_APPLICATION_KEY={os.getenv('OVH_APPLICATION_KEY')}")
print(f"export OVH_APPLICATION_SECRET={os.getenv('OVH_APPLICATION_SECRET')}")
print(f"export OVH_CONSUMER_KEY={str(validation['consumerKey'])}")
