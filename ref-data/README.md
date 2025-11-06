<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Tasks](#tasks)
- [Ontology and KG Best Practices](#ontology-and-kg-best-practices)
- [Thesaurus Data](#thesaurus-data)
    - [Thesaurus Orgs](#thesaurus-orgs)
    - [Tabular Thesaurus Data](#tabular-thesaurus-data)
        - [thes](#thes)
        - [org](#org)
        - [doc/data](#docdata)
        - [src](#src)
    - [Other Thesauri](#other-thesauri)
        - [ISO Languages](#iso-languages)

<!-- markdown-toc end -->

# Tasks
- [RES-253](https://graphwise.atlassian.net/browse/RES-253) CIRPASS (Cirpass2) Textiles DPP consulting
- [RES-271](https://graphwise.atlassian.net/browse/RES-271) crawl StandardsMap
- [RES-272](https://graphwise.atlassian.net/browse/RES-272) parse and extract UNECE Reference Guide on Code Lists and Identifiers in the Textile and Leather Value Chains

# Ontology and KG Best Practices

- We'll use a single (harmonized) namespace for all ontology terms and thesauri, with plentiful alignment links to other ontologies.
  It may be better to reuse existing terms directly, but that takes more time since we'd need to overcome (in some cases heavy) ontological baggage, and we don't have enough time for that
- CSV key fields should be suitable as both own URL (primary key), and link/reference (foreign key).
  Eg instead of `thes.url` (column `url` in table `thes`), we use `thes.thes_url`.
  This will make the concatenated `rdfpuml` model better connected, without the need to rename columns.
- External link fields should be called `weblink` to avoid confusion with `url` fields
- CSVs should use relative URLs. We'll use a common `prefixes.ttl` to add base and all needed prefixes.
- URLs should include words to indicate the nature of the resource at that URL. Eg
  - URLs in table `thes` start with `thes`
  - URLs in table `doc/data` start with `doc` or `data`
- Use hierarchical URLs, eg
  - `thes`: all thesauri
  - `thes/inventory`: thesauri related to inventories
  - `thes/inventory/reason`: thesauri related to the reason for some inventory operation
  - `thes/inventory/reason/movement`: reason for movement
  - `thes/inventory/reason/transport`: reason for transportation.
    Another good candidate is `thes/transport/reason`, because there are many others eg `thes/transport/mode` etc

# Thesaurus Data

## Thesaurus Orgs
TODO: flesh this out after filling the metadata table.

Here is a count of thesauri per organization, sorted in thematic order
| thes | items  | org             | name: thesaurus                                                                                       | format/comment                                 |
|------|--------|-----------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------|
|      |        | UNECE/UNCEFACT  |                                                                                                       | Plain text in HTML                             |
|      | 116.4k | UN LOCODE       | UN Location Codes (Rec16)                                                                             | [CSV, fixwidth, XML](https://unece.org/trade/cefact/UNLOCODE-Download). Turtle also available |
|      |        | UN UoM          | UN Units of Measurement (Rec20)                                                                       | [CSV](https://unece.org/trade/cefact/UNLOCODE-Download). Turtle also available                |
|      |        | UN Package Type | UN Package Type (Rec 21)                                                                              | [Excel](https://unece.org/sites/default/files/2021-06/rec21_Rev12e_Annex-V-VI_2021.xls)                                     |
|      |        | eBiz Mode-ML    |                                                                                                       | XML GeneriCode                                 |
|    1 |        | FAO             | Food and Agriculture Organization: crops                                                              | PDF: find as CSV/RDF                           |
|    2 | ~300   | ISO             | International Standardization Organization: country, language                                         | get from Wikidata                              |
|    1 | 900k   | CAS             | American Chemical Society: CAS id                                                                     | get from Wikidata? [900k populated](https://www.wikidata.org/wiki/Property_talk:P231)         |
|    1 | 106k   | ECHA            | European Chemicals Agency:  EC (REACH) id. eg benzene: EC number 200-753-7; ECHA Infocard 100.000.685 | get from Wikidata? [53% populated](https://www.wikidata.org/wiki/Property_talk:P232)          |
|    1 | ~300   | ZDHC            | Manufacturing restricted substance list (MRSL) for  Textile, Leather,  Polymers                       | [HTML](https://mrsl-30.roadmaptozero.com/), needs parsing                       |
|    1 |        | WHO             | WorldHealth Oganization: pesticides by hazard                                                         | [Forbidden](https://iris.who.int/rest/bitstreams/1278712/retrieve); [PDF](https://www.who.int/publications/i/item/9789240005662)                       |
|    1 | 34     | BCI             | Better Cotton Initiative: Pesticides classification                                                   | [Excel](https://bettercotton.org/wp-content/uploads/2014/01/Guidance-Pesticides-List-Classification.xlsx), keyed by CAS, complex structure    |
|   10 | ~400   | StdMap          | StandardsMap of sustainability standards. Thesauri extracted, standards not yet                       | HTML                                           |
|    1 | ~100k  | WCO HS          | World Customs Organization: Harmonized System                                                         | HTML/PDF: find as CSV/RDF                      |
|    1 | 14.6k  | EU CN           | EuroStat: Combined Nomenclature (listed as "Leather classification" p.16)                             | RDF->Turtle                                    |
|    1 | 22k    | GS1 GPC         | GS1 Global Product Classification: product hierarchy, attributes, enum values                         | JSON and JSON-LD                               |
|    1 |        | GTS             | Global Textile Scheme: GTS Language (GTS-L)                                                           | [info](https://www.globaltextilescheme.org/gts-standard/), [125 EUR/m](https://www.globaltextilescheme.org/pricing/)                      |

## Tabular Thesaurus Data
[thesauri](https://docs.google.com/spreadsheets/d/1kC1DnHEIsKaX39I31gkQyCJ4FqHbn9lDuZC3NEIP0mE/edit) is a google sheet where we collect thesaurus metadata.
The current structure is shown below, but it will evolve.

### thes
Thesauri

![](../img/csv-thes.png)

- `thes_url`: own thesaurus URL
- `name`: thesaurisi name
- `parent`: thesaurus parent URL
- `src`: source where the thesaurus was found.
  This can be a whole document, or document+locator

### org
Orgs that provide sustainability/DPP/trade/logistics thesauri and information

![](../img/csv-org.png)

- `org_url`: own org URL
- `abbrev`: abbreviation
- `name`: name
- `description`: description
- `weblink`: homepage

### doc/data
Web files (documents or data files)

![](../img/csv-doc.png)

- `doc_url`: own document URL
- `code`: identifier, eg "ECE/TRADE/C/CEFACT/2022/INF.1" (a particular UNECE doc), "UNCL 4499" (UN CodeList 4479)
- `title`: name
- `org_url`: organization that created/published the document
- `updated`: last updated date (if available)
- `version`: version (if available)
- `weblink`: web URL of the document
- `localFile`: local filename as saved in git
- `format`: MIME type
- `src_url`: source of info where this document/data was found
- `incomplete`: whether the data file is incomplete, since it was not obtained from a published location, but was scraped from the source document
- `task`: Jira task (won't be RDFized)

### src
Sources of information with locator (eg section, page) (DocumentPart)

![](../img/csv-src.png)

- `src_url`: own URL
- `doc_url`: document URL
- `locator`: descriptive location info (section, page, etc)

## Other Thesauri
The above 

### ISO Languages
Sec 4.16 Language and [UNCL 3453](https://service.unece.org/trade/untdid/d22a/tred/tred3453.htm) redirect to ISO 639-1 alpha2 language codes.
We can get alpha2 and alpha3 with this [Wikidata query](https://w.wiki/Fmkd):
```sparql
SELECT ?iso2 ?iso3 ?itemLabel WHERE {
  optional {?item wdt:P218 ?iso2}
  optional {?item wdt:P220 ?iso3}
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} order by ?iso2 ?iso3
```
