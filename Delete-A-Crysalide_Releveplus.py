import os  # pour récupérer les variables d'env
from typing import List

import ovh  # export ovh api
from decouple import config

# NEED TO DEFINE INCLUDED_DOMAIN
include_domains = ["crysalide.fr"]


class OVHClient:
    def __init__(self, application_key, application_secret, consumer_key):
        self.client = ovh.Client(
            endpoint="ovh-eu",
            application_key=config("ovh_application_key"),
            application_secret=config("ovh_application_secret"),
            consumer_key=config("ovh_consumer_key"),
        )

    def get_record_type_a(self, zone):
        records = self.client.get("/domain/zone/%s/record?fieldType=A" % zone)
        # print("get records : ", records)
        valid_records = []
        for record in records:
            r = self.get_record(zone, record)
            if r["target"].startswith("37.59.56.80"):
                valid_records.append(record)
        return valid_records

    def get_record(self, zone: str, record: str):
        return self.client.get("/domain/zone/%s/record/%s" % (zone, record))

    # def set_spf(self, zone: str, spf: str):
    #     record = self.get_record_type_a(zone)
    #     if not record:
    #         print("No spf %s for record %s" % (spf, zone))
    #     else:
    #         print("Delete spf %s for record %s" % (spf, zone))
    #         self.delete_record(zone, str(record))
    #     return

    # def delete_record(self, zone: str, record_id: str):
    #     return self.client.delete('/domain/zone/%s/record/%s' % (zone, record_id),)

    # def refresh_zone(self, zone: str):
    #     print("Refresh zone %s" % (zone))
    #     return self.client.post('/domain/zone/%s/refresh' % zone)

    def set_all(self):
        for zo in include_domains:
            print("zones : ", zo)
            print("type of zones : ", type(zo))
            print("records", self.get_record_type_a(zo))
            print("type of records", type(self.get_record_type_a(zo)))
            # for record_a in self.get_record_type_a(zo):
            # self.get_record(zo, record_a)
            # self.delete_record(zo, a)
            # self.refresh_zone(zo)


client = OVHClient(application_key="", application_secret="", consumer_key="")
client.set_all()
