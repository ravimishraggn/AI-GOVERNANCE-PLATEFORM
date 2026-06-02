# SEC Compliance Pack

First-party governance plugin providing compliance controls for SEC-regulated investment advisers.

## Covered Frameworks

| Framework | Coverage |
|-----------|---------|
| SR 11-7 / OCC 2011-12 | Model risk management, validation, inventory |
| SEC Rule 17a-4 | Books and records, immutability requirements |
| FINRA Rule 4511 | Record retention for member firms |
| SEC Regulation BI | Best interest standard for AI-assisted advice |

## Controls Provided

- Model inventory completeness check (SR 11-7 inventory requirement)
- Model validation independence verification (SR 11-7 section III)
- Ongoing monitoring requirement enforcement (SR 11-7 section III)
- Records immutability verification (17a-4 WORM requirement)
- Retention period enforcement by record class
- Supervisory system documentation check (FINRA)
- Best interest analysis documentation (Reg BI)

## Activation

```bash
governance-cli plugins activate sec-compliance-pack \
  --tenant your-tenant-id \
  --frameworks [sr-11-7, sec-17a4, finra-4511]
```

Requires compliance officer authorization.
