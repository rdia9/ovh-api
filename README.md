# OVH API

[![GitHub Super-Linter](https://github.com/rdia9/ovh-api/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

Ce repository permet des extractions simplifiées via l'API OVH

## Requirements

### 📍 Location

IP from OVH or SQY

### 🛠️ Packages

- python
- pip install ovh
- .env with completed with values
  - ovh_endpoint (ovh-eu)
  - ovh_application_key (keepass)
  - ovh_application_secret (keepass)
  - ovh_consumer_key (keepass)

To create OVH API credentials go there <https://eu.api.ovh.com/createToken/>
// It needs the following Endpoints :
// - GET /domain/zone
// - GET /domain/zone/*/record
// - GET /domain/zone/*/record/*
// - PUT /domain/zone/*/record/*
// - POST /domain/zone/*/record

## Execution

```bash
pip3 install -r requirement.txt
python3 List-Domains.py > DomainsList.csv
python3 List-DNSZoneIsnDomains.py > DNSZonesList.csv
python3 Update-SPFrecords_include.py > UpdateSPFrecords_include.log # Noter dans le script les domaines à inclure
python3 Update-SPFrecords_exclude.py > UpdateSPFrecords_exclude.log # Noter dans le script les domaines à exclure
python3 Update-DMARCrecords_include.py > UpdateDMARCrecords_include.log # Noter dans le script les domaines à inclure
python3 Update-DMARCrecords_exclude.py > UpdateDMARCrecords_exluded.log # Noter dans le script les domaines à exclure
python3 Enable-DNSSEC.py > EnableDNSSEC.log
```

## ✒️ Authors

[Raphaël Diacamille](https://github.com/rdia9) \
[Paul Baudrier](https://github.com/paulbaudrier) \
[Paul Waldburger](https://github.com/Paul-Waldburger-BTPConsultants)
