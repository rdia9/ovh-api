from typing import List
import ovh  # export ovh api
import os  # pour récupérer les variables d'env
from decouple import config

print ("This script only works on OVH or SQY network.")

include_domains = ["citybuildr.io"]
dmarc_value = str("v=DMARC1; p=reject; rua=mailto:rsi@btp-consultants.fr; ruf=mailto:rsi@btp-consultants.fr; rf=afrf; pct=100; ri=86400")


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
        return [i for i in zones if i in include_domains]

    def get_dmarc(self, zone):
        records = self.client.get('/domain/zone/%s/record?fieldType=DMARC'
                                % zone)
        for record in records:
            r = self.get_record(zone, record)
            if r["target"].startswith("v=DMARC1"):
                return record
        return

    def get_record(self, zone: str, record: str):
        return self.client.get('/domain/zone/%s/record/%s' % (zone, record))

    def set_record(self, zone, value):
        return self.client.post('/domain/zone/%s/record' % zone,
                                target=value,
                                fieldType="DMARC",
                                ttl=3600,
                                subDomain="_dmarc")

    def set_dmarc(self, zone: str, dmarc: str):
        record = self.get_dmarc(zone)
        if not record:
            print("Setting dmarc %s for record %s" % (dmarc, zone))
            self.set_record(zone, dmarc)
        else:
            print("Updating dmarc %s for record %s" % (dmarc, zone))
            self.update_record(zone, dmarc_value, str(record))
        return

    def update_record(self, zone: str, value: str, record_id: str):
        return self.client.put('/domain/zone/%s/record/%s' % (zone, record_id),
                            target=value,
                            ttl=3600)

    def refresh_zone(self, zone: str):
        print("Refresh zone %s" % (zone))
        return self.client.post('/domain/zone/%s/refresh' % zone)

    def set_dmarc_all(self, dmarc: str):
        for zo in self.get_zones():
            self.set_dmarc(zo, dmarc)
            self.refresh_zone(zo)


client = DMARCClient(application_key="", application_secret="",
                    consumer_key="")
client.set_dmarc_all(dmarc_value)