

from typing import List
import ovh # export ovh api
import os # pour récupérer les variables d'env
from decouple import config

# "prevention-consultants.com" is the only one not excluded for test
exclude_domains = ["crysalide.fr","nextiim.com","citybuildr.io","parkyze.org","monitoring-environnemental.fr","batily.eu","btpdiagnostics.com","parkyze.net","btp-diagnostics.com","btp-consultants-monaco.fr","naval-check.com","btpdiagnostic.com","batidigi.fr","parkyze.fr","btpdiagnostic.fr","btp-diagnostic.fr","databuildr.com","groupe-btp-consultants.fr","btp-consultants.fr","batidigi.com","naval-check.fr","signaletique-for-all.fr","btp-mornings.fr","citybuildr.com","bimscreen.com","deepbim.fr","batily.org","databuildr.net","btp-consultants.com","batily.fr","parkyze.co","novalian.io","citybuild.fr","btpdiagnostics.fr","batidigi.ovh","batidigi.org","faqplus.fr","bet-accessibilite.com","btp-consultants.net","batidigi.eu","formactu.com","databuildr.ovh","batily.cloud","databuildr.eu","deepbim.io","btp-diagnostic.com","databuildr.cloud","groupe-btp-consultants.com","batily.net","databuildr.org","groupe-btpconsultants.com","batidigi.cloud","batily.ovh","databuildr.fr","parkyze.eu","citae.fr","parkyze.in","btp-mornings.com","mbacity.com","formactu.fr","parkyze.com","novalian.fr","btp-diagnostics.fr","navalcheck.fr","groupe-btpconsultants.fr","prevention-consultants.net","groupe-btp.fr","batiment-numerique-bimpourtous.fr","parkyze.io","mbacity.fr","citae-patrimoine.com","navalcheck.com","bimscreen.fr","betaccessibilite.com","groupebtp.com","batidigi.net","groupebtp.fr","btp-consultants.org","batiment-numerique-bimpourtous.com","bet-access.com","citae-patrimoine.fr","groupe-btp.com","citybuildr.fr","batily.com"]
# exclude_domains = ["btp-consultants.fr","citae.fr","mbacity.com","btp-diagnostics.fr","groupebtp.fr"]
spf_value = "\"v=spf1 ip4:37.59.248.160/28 ip4:185.183.65.201 include:_spf.google.com include:amazonses.com ~all\""

"""
To create OVH api credentials go there https://eu.api.ovh.com/createToken/
// It needs the following Endpoints :
// - GET /domain/zone
// - GET /domain/zone/*/record
// - GET /domain/zone/*/record/*
// - PUT /domain/zone/*/record/*
// - POST /domain/zone/*/record
"""

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
        return self.client.post('/domain/zone/%s/record' % zone, target=value, fieldType="SPF", ttl=60)

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
        return self.client.put('/domain/zone/%s/record/%s' % (zone, record_id), target=value)

    def set_spf_all(self, spf: str):
        for zo in self.get_zones():
            self.set_spf(zo, spf)


client = SPFClient(application_key="", application_secret="",
                   consumer_key="")
client.set_spf_all(spf_value)
