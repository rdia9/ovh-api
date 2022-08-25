from typing import List
import ovh # export ovh api
import os # pour récupérer les variables d'env
from decouple import config

inclued_domains = ["parkyze.net"]

class OVHClient:
    def __init__(self, application_key, application_secret, consumer_key):
        self.client = ovh.Client(
            endpoint="ovh-eu",
            application_key=config('ovh_application_key'),
            application_secret=config('ovh_application_secret'),
            consumer_key=config('ovh_consumer_key'),
        )

    def get_zones(self) -> List[str]:
        zones = self.client.get("/domain/zone")
        return [i for i in zones if i in inclued_domains]

    def set_dnssec(self, zone :str):
        print("Setting DNSSEC for domain %s" % (zone))
        return self.client.post('/domain/zone/%s/dnssec' % zone)

    # def refresh_zone(self, zone: str):
    #     print("Refresh zone %s" % (zone))
    #     return self.client.post('/domain/zone/%s/refresh' % zone)

    def set_dnssec_all(self):
        for zo in self.get_zones():
            self.set_dnssec(zo)

client = OVHClient(application_key="", application_secret="",
                   consumer_key="")
client.set_dnssec_all()
