# UNCEFACT Code Lists

The [UneceRefGuide](./UneceRefGuide) lists 17-18 UNCEFACT Code Lists, which are one of the main sources for textile taxonomies.
(The other main source is [eBiz](../eBiz).)

For example, `<inventory/reason/movement>` comes from [UNCL4499](https://service.unece.org/trade/untdid/d22a/tred/tred4499.htm).
These are plain text data embedded in HTML that looks like this:
```
     Code Values: 

     1     Reception
              Goods received at warehouse from another party or
              warehouse.

     2     Delivery
              Goods which have been delivered from the inventory to
              another party or warehouse.
```

## Extraction

NOTE(vsenderov, 2026-01-22): Don't rerun the extractors unless you absolutely need to. The TSV's have been manually edited 
to remove spelling errors and other inconsistencies.

We use a Python script `uncl_extract.py` to extract the item lists.
First build the python environment:
```
  ./uncl-extract.sh build
```

Then run the program for every UNCL code list. Eg this downloads `UNCL4499.htm`:
```
  ./uncl-extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4499.htm
```
It then extracts the data and outputs `UNCL4499.tsv` that looks like:
| code | name      | descr                                                                             |
|------|-----------|-----------------------------------------------------------------------------------|
|    1 | Reception | Goods received at warehouse from another party or warehouse.                      |
|    2 | Delivery  | Goods which have been delivered from the inventory to another party or warehouse. |

## RDFization

We use SPARQL Anything so that we can specify query parameters on the command line:
`thes` which gets mapped to the variable `$_thes_iri`.
We call it like this:
```
sparql-anything -v location=UNCL4499.tsv -o UNCL4499.ttl -v thes=inventory/reason/movement -q uncl_convert.rq
```

This produces RDF files like this:
```ttl
<https://w3id.org/eudpp/thesauri/inventory/reason/movement/1>
        rdf:type         skos:Concept;
        skos:definition  "Goods received at warehouse from another party or warehouse.";
        skos:notation    "1";
        skos:prefLabel   "Reception" .

<https://w3id.org/eudpp/thesauri/inventory/reason/movement>
        skos:member  <https://w3id.org/eudpp/thesauri/inventory/reason/movement/11>, ...  <https://w3id.org/eudpp/thesauri/inventory/reason/movement/1> .
```
