import os  # pour récupérer les variables d'env
from typing import List

import ovh  # export ovh api
from decouple import config

included_domains = ["parkyze.in", "bet-access.com", "mbacity.fr"]


class OVHClient:
    def __init__(self, application_key, application_secret, consumer_key):
        self.client = ovh.Client(
            endpoint="ovh-eu",
            application_key=config("OVH_APPLICATION_KEY"),
            application_secret=config("OVH_APPLICATION_SECRET"),
            consumer_key=config("OVH_CONSUMER_KEY"),
        )

    def get_zones(self) -> List[str]:
        zones = self.client.get("/domain/zone")
        return [i for i in zones if i in included_domains]

    def set_dnssec(self, zone: str):
        print("Getting DNSSEC for domain %s" % (zone))
        status_dnssec = str(self.client.get("/domain/zone/%s/dnssec" % zone))
        print(status_dnssec)
        if "enableInProgress" in status_dnssec:
            print("DNSSEC is already in progress for domain %s" % (zone))
        elif "disabled" in status_dnssec:
            print("Enabling DNSSEC for domain %s" % (zone))
            return self.client.post("/domain/zone/%s/dnssec" % zone)
        else:
            print("DNSSEC is already activated for domain %s" % (zone))

    def set_dnssec_all(self):
        for zzone in self.get_zones():
            self.set_dnssec(zzone)


client = OVHClient(application_key="", application_secret="", consumer_key="")
client.set_dnssec_all()
