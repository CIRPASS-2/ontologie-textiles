# Data

## StdMap.md

Obtained by manual browsing of the net. Not used.

## cc-cname-mapping-2025-12-15.csv

Mapping of country codes to country names. Downloaded from an authoritative source on the web on Dec 15 2025.

## stdmap-uncorrected.JSON

Download of StandardsMap from their API (Stage 1)

    https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION


## stdmap.JSON

Manual edits (spelling corrections and such) done on `stdmap-uncorrected.JSON`.

## stdmap.csv

Obtained from running Stage 2a on the manually edited `stdmap.JSON`

## country-destination.txt, country-origin.txt and mandate.txt

Obtained by running

    csvtk cut -f origin      stdmap.csv|perl -pe 's{;}{\n}g'|sort|uniq>country-origin.txt
    csvtk cut -f destination stdmap.csv|perl -pe 's{;}{\n}g'|sort|uniq>country-destination.txt
    csvtk cut -f mandate     stdmap.csv|perl -pe 's{;}{\n}g'|sort|uniq -c|sort -rn>mandate.txt
