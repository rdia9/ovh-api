
import os  # pour récupérer les variables d'env
import ovh  # export ovh api
from decouple import config
from typing import List

included_domains = ["navalcheck.fr"]


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
        return [i for i in zones if i in included_domains]

    def get_dnssec(self, zone):
        print("Getting DNSSEC for domain %s" % (zone))
        return self.client.get('/domain/zone/%s/dnssec' % zone)

    def set_dnssec(self, zone: str):
        record = self.get_dnssec(zone)
        if not record:
            print("Setting DNSSEC for domain %s" % (zone))
            return self.client.post('/domain/zone/%s/dnssec' % zone)
        else:
            print(" DNSSEC for domain %s already activated" % (zone))
        return

    def set_dnssec_all(self):
        for zzone in self.get_zones():
            self.set_dnssec(zzone)


client = OVHClient(application_key="", application_secret="",
                   consumer_key="")
client.set_dnssec_all()