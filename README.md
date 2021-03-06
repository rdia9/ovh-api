[![GitHub Super-Linter](https://github.com/rdia9/ovh-api/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

# ovh-api

Ce repository permet des extractions simplifiées via l'API OVH

## Requirements

- python
- pip install ovh
- .env with completed with values
  - ovh_endpoint
  - ovh_application_key
  - ovh_application_secret
  - ovh_consumer_key

## Execution

```bash
python3 List-Domain.py > DomainList.csv
python3 List-DNSZoneInDomain.py > DNSZoneList.csv
```

## ✒️ Authors

[Raphaël Diacamille](https://github.com/rdia9) \
[Paul Baudrier](https://github.com/paulbaudrier) \
[Paul Waldburger](https://github.com/Paul-Waldburger-BTPConsultants)
