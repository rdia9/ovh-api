# from typing import List
# import ovh # export ovh api
# import os # pour récupérer les variables d'env
# from decouple import config

## NEED TO DEFINE EXCLUDE_DOMAIN
# exclude_domains = [domain1, domain2, etc]

# class SPFClient:
#     def __init__(self, application_key, application_secret, consumer_key):
#         self.client = ovh.Client(
#             endpoint="ovh-eu",
#             application_key=config('ovh_application_key'),
#             application_secret=config('ovh_application_secret'),
#             consumer_key=config('ovh_consumer_key'),
#         )

#     def get_zones(self) -> List[str]:
#         zones = self.client.get("/domain/zone")
#         return [i for i in zones if i not in exclude_domains]

#     def get_spf(self, zone):
#         records = self.client.get('/domain/zone/%s/record?fieldType=TXT' % zone)
#         for record in records:
#             r = self.get_record(zone, record)
#             if r["target"].startswith("\"v=spf1"):
#                 return record
#         return

#     def get_record(self, zone: str, record: str):
#         return self.client.get('/domain/zone/%s/record/%s' % (zone, record))

#     def set_spf(self, zone: str, spf: str):
#         record = self.get_spf(zone)
#         if not record:
#             print("No spf %s for record %s" % (spf, zone))
#         else:
#             print("Delete spf %s for record %s" % (spf, zone))
#             self.delete_record(zone, str(record))
#         return

#     def delete_record(self, zone: str, record_id: str):
#         return self.client.delete('/domain/zone/%s/record/%s' % (zone, record_id),)

#     def refresh_zone(self, zone: str):
#         print("Refresh zone %s" % (zone))
#         return self.client.post('/domain/zone/%s/refresh' % zone)

#     def set_spf_all(self, spf: str):
#         for zo in self.get_zones():
#             self.set_spf(zo, spf)
#             self.refresh_zone(zo)

# client = SPFClient(application_key="", application_secret="",
#                    consumer_key="")
# client.set_spf_all(spf_value)
