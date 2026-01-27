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

## Exploring Levels and Code Length
All [EuroStat classifications](https://ec.europa.eu/eurostat/web/metadata/classifications) use the [XKOS ontology](https://rdf-vocabulary.ddialliance.org/xkos.html) which is an extension of SKOS.
In particular, it expresses the level (depth) of each node using `xkos:depth`.

Let's see the distribution of codes by level:
```
perl -ne 'm{xkos:depth +"(\d+)"} and print "$1\n"' cn.ttl |sort -n|uniq -c
     22 1
     99 2
   1264 3
   3648 4
   5178 5
   3054 6
   1282 7
    568 8
    204 9
    132 10
     63 11
```

We can explore nodes at the deepest level 11 like this (the weird double-in-single-quotes mean: search for `"11"`).
```
less '+/"11"' cn.ttl
```


The first match is `cn2021:220421380080`
- It is defined like this (I kid you not!)
> "White wines produced in EU, in containers holding <= 2 l and of an actual alcoholic strength of <= 15% vol, with PDO (other than Alsace, Bordeaux, Bourgogne, Val de Loire, Mosel, Pfalz, Rheinhessen, Tokaj, Lazio, Toscana, Trentino, Alto Adige, Friuli, Veneto, Sicilia, vinho verde, Penedés, Rioja, Valencia, sparkling wine and semi-sparkling wine)"@en
- Its code (`dc:identifier` and URL) has 12 digits
- But its `skos:notation "2204 21 38"` has 8 digits and is used only once in the whole file:
```
grep -cP 'skos:notation +"2204 21 38"' cn.ttl
1
```
- Its parent is `skos:broader cn2021:220421110050` "Wine with a protected designation of origin (PDO) - White wines"
  and has `dc:identifier` but not `skos:notation`(?)

If we explore all notations:
```
perl -ne 'm{skos:notation +"(.+?)"} and print "$1\n"' cn.ttl |sort|uniq |less
```

We see the typical CN hierarchical structure:
```
01
0101
0101 21 00
0101 29
0101 29 10
0101 29 90
0101 30 00
0101 90 00
```
Plus a few more codes for CN itself, and for its chapters:
```
CN 2021
I
II
III
...
```
No notation is used more than once.

In summary:
- CN codes (`skos:notation`) have length 2,4,6 or 8 decimals (with some spaces added for readability)
- CN identifiers (`dc:identifier`) always have length 12 decimals.
  - Shorter codes are padded with `0`
  - I think the last 4 are check digits (all but one are zeros)
