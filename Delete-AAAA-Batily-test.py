import json
import os  # pour récupérer les variables d'env
from typing import List

import ovh  # export ovh api
from decouple import config

###############################################################
#           RENSEIGNEZ LE(S) NOM(S) DE DOMAINES               #
###############################################################
include_domains = ["batily.org"]

###############################################################
#           RENSEIGNEZ L'ADRESSE IP A SUPPRIMER               #
###############################################################
address_to_delete = "mettre_ici_l_ipv6_à_supprimer"


class OVHClient:
    def __init__(self, application_key, application_secret, consumer_key):
        self.client = ovh.Client(
            endpoint="ovh-eu",
            application_key=config("OVH_APPLICATION_KEY"),
            application_secret=config("OVH_APPLICATION_SECRET"),
            consumer_key=config("OVH_CONSUMER_KEY"),
        )

    def get_record_type_aaaa(self, zone):
        records = self.client.get("/domain/zone/%s/record?fieldType=AAAA" % zone)
        valid_records = []
        for record in records:
            r = self.get_record(zone, record)
            if r["target"] == address_to_delete:
                valid_records.append(record)
        return valid_records

    def get_record(self, zone: str, record: str):
        return self.client.get("/domain/zone/%s/record/%s" % (zone, record))

    def delete_record(self, zone: str, record_id: str):
        return self.client.delete(
            "/domain/zone/%s/record/%s" % (zone, record_id),
        )

    def refresh_zone(self, zone: str):
        return self.client.post("/domain/zone/%s/refresh" % zone)

    def set_all(self):
        for zo in include_domains:
            print()
            print("#####################################")
            print("Zone :", zo)
            print("#####################################")
            print()
            print("List of records ID to delete:", self.get_record_type_aaaa(zo))
            print("")
            for record_a in self.get_record_type_aaaa(zo):
                print("---------------------------")
                print("Record", record_aaaa, "details :")
                print("---------------------------")
                display = self.get_record(zo, record_aaaa)
                print(json.dumps(display, indent=4, sort_keys=True))
                print()
                self.delete_record(zo, record_aaaa)
            print("All records in the list have been successfully deleted.")
            print()
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("Refreshing zone :", zo)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print()
            self.refresh_zone(zo)
        print("Script ended successfully")

client = OVHClient(application_key="", application_secret="", consumer_key="")
client.set_all()