# Combined Nomenclature

- description: https://trade.ec.europa.eu/access-to-markets/en/content/combined-nomenclature-0
  - classifying leather goods: https://trade.ec.europa.eu/access-to-markets/en/content/classifying-leather
- dataset: https://data.europa.eu/data/datasets/combined-nomenclature-2021
  - Note: The download links are broken in all newer versions:
    https://data.europa.eu/data/datasets/combined-nomenclature-2022 ,
    https://data.europa.eu/data/datasets/combined-nomenclature-2023 ,
    https://data.europa.eu/data/datasets/combined-nomenclature-2024 ,
    https://data.europa.eu/data/datasets/combined-nomenclature-2025

- download SKOS core https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/combined-nomenclature-2021/20241120-0/rdf/skos_core/ESTAT-CN2021.rdf&fileName=ESTAT-CN2021.rdf
  - RDF 5.4Mb, Turtle

```
curl -o ESTAT-CN.rdf "https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/combined-nomenclature-2021/20241120-0/rdf/skos_core/ESTAT-CN2021.rdf&fileName=ESTAT-CN2021.rdf"
riot --formatted ttl ESTAT-CN.rdf > ESTAT-CN.ttl
cat prefixes.ttl ESTAT-CN.ttl > ESTAT-CN-prefixed.ttl
owl write ESTAT-CN-prefixed.ttl cn.ttl
```
