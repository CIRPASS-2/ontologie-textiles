---
title: Textile-related Ontologies and Taxonomies
author: Vladimir Alexiev
date: 2025-10-19
---

* Ontologies and Taxonomies
** GS1 GPC
- JSON: official release from https://gpc-browser.gs1.org/ , saved as [GS1-GPC-20250509-GB.json](GS1-GPC-20250509-GB.json) (33Mb)
- JSON-LD: from https://mh1.eu/gpctest/ , embedded in the web page: [GS1-GPC-test.jsonld](GS1-GPC-test.jsonld) (10Mb)
```
# prettify JSON (33 -> 81.5Mb)
jq . GS1-GPC-20250509-GB.json > GS1-GPC-20250509-pretty.json
# prettify JSON-LD (10 -> 17.5Mb)
jq . GS1-GPC-test.jsonld > GS1-GPC-test-pretty.jsonld
# convert to Turtle
riot --out ttl GS1-GPC-test.jsonld > GS1-GPC-test.ttl
# prettify Turtle (takes a few minutes because it builds the complete RDF model in memory) (8Mb)
owl write --useCommaByDefault GS1-GPC-test.ttl GS1-GPC-test-pretty.ttl
```

TODO: there is some problem with the JSON-LD file or conversion.
```
grep -oP '"Code": \d+' GS1-GPC-20250509-pretty.json|sort|uniq -c > nodes-json.txt
grep      '"@id": "gpc:'  GS1-GPC-test-pretty.jsonld|sort > nodes-jsonld.txt
grep -aoP 'gpc:[0-9]+ a ' GS1-GPC-test-pretty.ttl   |sort > nodes-ttl.txt
wc -l node*
  22182 nodes-json.txt
 194542 nodes-jsonld.txt
   9474 nodes-ttl.txt
```

GPC objects (bricks) have props (attributes) that share common names and enum lists, but the lists are localized (subset) per class.
Take for example:

gpc:10005176 Fancy Dress Accessories (Powered)
- Subclass of gpc:86010500 Fancy Dress Costumes/Accessories
- Attributes
  - gpc:20002171 Type of Fancy Dress Accessory (Powered)
  - gpc:20000045 Consumer Lifestage
  - gpc:20000366 Target Gender <<< let's look at this general attribute

```ttl
gpc:86010500 a gpc:Class;
  rdfs:label "Fancy Dress Costumes/Accessories"@en;
  rdfs:subClassOf "gpc:86010000",
gpc:10005176 a gpc:Brick,
  rdfs:label: "Fancy Dress Accessories (Powered)"@en,
  rdfs:subClassOf gpc:86010500.
gpc:20000366 a rdf:Property, gpc:Attribute ;
  rdfs:label "Target Gender"@en ;
gpc:30003891 a gpc:AttributeValue,
  rdfs:label "FEMALE"@en.

_:a20000366b10005176
  rdfs:domain gpc:10005176 ;
  rdfs:range [
    a owl:Class ;
    owl:unionOf gpc:30002515, gpc:30002518, gpc:30003891, gpc:30004039, gpc:30004340 ;
  ] ;
  rdfs:subPropertyOf gpc:20000366.
```
This uses an unusual construct in that it defines a blank-node property that is subprop of the general attribute, but defines a specific enumerated range.
Note: `owl:unionOf` is a mistake, should be `owl:oneOf` and use a list instead of multivalued property.
