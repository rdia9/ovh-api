# OVH API

[![GitHub Super-Linter](https://github.com/rdia9/ovh-api/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/rdia9/ovh-api/actions/workflows/linter.yml)

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

To create OVH API credentials go there <https://eu.api.ovh.com/createToken/> \
 It needs the following Endpoints :

- GET /domain/zone
- GET /domain/zone/*/record
- GET /domain/zone/*/record/*
- PUT /domain/zone/*/record/*
- POST /domain/zone/*/record

### Python

```pip3 install -r requirement.txt```

## Execution

- Inventorier

```bash
# Lister les domaines
python3 List-Domains.py > DomainsList.csv
```

```bash
# Lister les Urls publiées
python3 List-DNSZoneIsnDomains.py > DNSZonesList.csv
```

- Action sur les SPF

```bash
python3 Update-SPFrecords_include.py > UpdateSPFrecords_include.log
# Noter dans le script les domaines à inclure

python3 Update-SPFrecords_exclude.py > UpdateSPFrecords_exclude.log
# Noter dans le script les domaines à exclure
```

- Action sur les DMARC

```bash
python3 Update-DMARCrecords_include.py > UpdateDMARCrecords_include.log
# Noter dans le script les domaines à inclure

python3 Update-DMARCrecords_exclude.py > UpdateDMARCrecords_exluded.log
# Noter dans le script les domaines à exclure
```

- Action sur les DNSSEC

```bash
python3 Enable-DNSSEC_exclude > EnableDNSSEC_excluded.log
# Noter dans le script les domaines à exclure

python3 Enable-DNSSEC_include > EnableDNSSEC_included.log
# Noter dans le script les domaines à inclure
```

- Action sur une IP spécifique

```bash
python3 Delete-A-Batily-test.py > delete-Releveplus.log
# Renseigner le/les domaine(s) dans le script ainsi que l'IP à supprimer
```

## ✒️ Authors

[Raphaël Diacamille](https://github.com/rdia9) \
[Paul Baudrier](https://github.com/paulbaudrier)
