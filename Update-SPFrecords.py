from typing import List
import ovh # export ovh api
import os # pour récupérer les variables d'env
from decouple import config

exclude_domains = ["btp-consultants.fr","citae.fr","mbacity.com","btp-diagnostics.fr","groupebtp.fr"]
spf_value = str("v=spf1 ip4:37.59.248.160/28 ip4:185.183.65.201 include:_spf.google.com include:amazonses.com ~all")
class SPFClient:
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

    def get_spf(self, zone):
        records = self.client.get('/domain/zone/%s/record?fieldType=SPF' % zone)
        for record in records:
            r = self.get_record(zone, record)
            if r["target"].startswith("\"v=spf1"):
                return record
        return

    def get_record(self, zone: str, record: str):
        return self.client.get('/domain/zone/%s/record/%s' % (zone, record))

    def set_record(self, zone, value):
        return self.client.post('/domain/zone/%s/record' % zone, target=value, fieldType="SPF", ttl=3600)

    def set_spf(self, zone: str, spf: str):
        record = self.get_spf(zone)
        if not record:
            print("Setting spf %s for record %s" % (spf, zone))
            self.set_record(zone, spf)
        else:
            print("Updating spf %s for record %s" % (spf, zone))
            self.update_record(zone,spf_value, str(record))
        return

    def update_record(self, zone: str, value: str, record_id: str):
        return self.client.put('/domain/zone/%s/record/%s' % (zone, record_id), target=value, ttl=3600)

    def refresh_zone(self, zone: str):
        print("Refresh zone %s" % (zone))
        return self.client.post('/domain/zone/%s/refresh' % zone)

    def set_spf_all(self, spf: str):
        for zo in self.get_zones():
            self.set_spf(zo, spf)
            self.refresh_zone(zo)

client = SPFClient(application_key="", application_secret="",
                   consumer_key="")
client.set_spf_all(spf_value)
