# DNS-Sovereignty
Traffic Centralization and Digital Sovereignty: An Analysis Under the Lens of DNS Servers

Developers: Demétrio Boeira and Luciano Zembruski

Project Managers: Dr. Muriel F. Franco (mffranco@inf.ufrgs.br) and Dr. Eder J. Scheid (ejscheid@inf.ufrgs.br)

Computer Networks Group (Head: Prof. Dr. Lisandro Zambenedetti Granville)

Repository Structure:

```bash
├── README.md % This README
├── asn-country-lookup.py % Script to enrich the Tranco list
├── downloader.py % Script to download datasets and the Tranco list
├── measurement.py % Script to perform the measurements
├── dataset % Datasets used in the paper
│   ├── ipasn_230616.dat
│   ├── tranco_230616.csv
│   └── tranco_230616-enriched.csv
└── results % Results of the paper
    ├── centralization
    │   ├── Period 1
    │   │   ├── concentration-2022-12-16
    │   │   ├── concentration-2022-12-17
    │   │   ├── concentration-2022-12-19
    │   │   └── concentration-2022-12-24
    │   ├── Period 2
    │   │   ├── concentration-2023-01-23
    │   │   ├── concentration-2023-01-29
    │   │   └── concentration-2023-02-08
    │   └── Period 3
    │       ├── concentration-2023-03-02
    │       ├── concentration-2023-03-07
    │       └── concentration-2023-03-15
    └── raw data - charts % Raw data used to build the charts
        ├── brasil.csv
        ├── brasil-gov-br.csv
        ├── brics.csv
        ├── china.csv
        ├── china-gov-cn.csv
        ├── concentration.csv
        ├── eu.csv
        ├── india.csv
        ├── india-gov-in.csv
        ├── south-africa.csv
        └── south-africa-gov-za.csv
```
