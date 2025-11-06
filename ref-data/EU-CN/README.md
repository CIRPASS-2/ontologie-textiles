# Combined Nomenclature

The EU The Combined Nomenclature (CN) is the EU's eight-digit coding system, 
comprising the WCO Harmonised System (HS) codes with further EU subdivisions. 
It serves the EU's common customs tariff and provides statistics for trade within the EU and between the EU and the rest of the world.

- description: https://trade.ec.europa.eu/access-to-markets/en/content/combined-nomenclature-0
  - classifying leather goods: https://trade.ec.europa.eu/access-to-markets/en/content/classifying-leather
- dataset: https://data.europa.eu/data/datasets/combined-nomenclature-2021
  - Note: The download links are broken in all newer versions:
    https://data.europa.eu/data/datasets/combined-nomenclature-2022 ,
    https://data.europa.eu/data/datasets/combined-nomenclature-2023 ,
    https://data.europa.eu/data/datasets/combined-nomenclature-2024 ,
    https://data.europa.eu/data/datasets/combined-nomenclature-2025

- download SKOS core (RDF 5.4Mb) https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/combined-nomenclature-2021/20241120-0/rdf/skos_core/ESTAT-CN2021.rdf&fileName=ESTAT-CN2021.rdf
- Convert to Turtle
- Add prefixes
- Write in a prettified form `cn.ttl` (Turtle 78Mb)

```
curl -o ESTAT-CN.rdf "https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/combined-nomenclature-2021/20241120-0/rdf/skos_core/ESTAT-CN2021.rdf&fileName=ESTAT-CN2021.rdf"
riot --formatted ttl ESTAT-CN.rdf > ESTAT-CN.ttl
cat prefixes.ttl ESTAT-CN.ttl > ESTAT-CN-prefixed.ttl
owl write ESTAT-CN-prefixed.ttl cn.ttl
```
