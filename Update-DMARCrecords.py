from typing import List
import ovh # export ovh api
import os # pour récupérer les variables d'env
from decouple import config

exclude_domains = ["btp-consultants.fr","citae.fr","mbacity.com","btp-diagnostics.fr","groupebtp.fr"]
dmarc_value = "\"v=DMARC1; p=reject; rua=mailto:dmarc@mailinblue.com!10m; ruf=mailto:dmarc@mailinblue.com!10m; rf=afrf; pct=100; ri=86400\""

"""
To create OVH api credentials go there https://eu.api.ovh.com/createToken/
// It needs the following Endpoints :
// - GET /domain/zone
// - GET /domain/zone/*/record
// - GET /domain/zone/*/record/*
// - PUT /domain/zone/*/record/*
// - POST /domain/zone/*/record
"""

class DMARCClient:
    def __init__(self, application_key, application_secret, consumer_key):
        self.client = ovh.Client(
            endpoint="ovh-eu",
            application_key=config('ovh_application_key'),
            application_secret=config('ovh_application_secret'),
            consumer_key=config('ovh_consumer_key'),
        )

    def get_zones(self) -> List[str]:
        zones = self.client.get("/domain/zone")
        return [i for i in zones if i not in exclude_domains]

    def get_dmarc(self, zone):
        records = self.client.get('/domain/zone/%s/record?fieldType=DMARC' % zone)
        for record in records:
            r = self.get_record(zone, record)
            if r["target"].startswith("\"v=DMARC1"):
                return record
        return

    def get_record(self, zone: str, record: str):
        return self.client.get('/domain/zone/%s/record/%s' % (zone, record))

    def set_record(self, zone, value):
        return self.client.post('/domain/zone/%s/record' % zone, target=value, fieldType="DMARC", ttl=3600)

    def set_dmarc(self, zone: str, dmarc: str):
        record = self.get_dmarc(zone)
        if not record:
            print("Setting dmarc %s for record %s" % (dmarc, zone))
            self.set_record(zone, dmarc)
        else:
            print("Updating dmarc %s for record %s" % (dmarc, zone))
            self.update_record(zone,dmarc_value, str(record))
        return

    def update_record(self, zone: str, value: str, record_id: str):
        return self.client.put('/domain/zone/%s/record/%s' % (zone, record_id), target=value)

    def set_dmarc_all(self, dmarc: str):
        for zo in self.get_zones():
            self.set_dmarc(zo, dmarc)


client = DMARCClient(application_key="", application_secret="",
                   consumer_key="")
client.set_dmarc_all(dmarc_value)
