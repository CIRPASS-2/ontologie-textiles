# Convert eBiz genericode XML

We use https://github.com/SPARQL-Anything , which is a brilliant tool for converting all kind of formats to Turtle.
See this paper: https://www.semantic-web-journal.net/content/materialisation-approaches-façade-based-data-access-sparql-0 .

To convert XML Genericode from eBiz to SKOS, we use this very simple query:
```
base         <https://cirpass.eu/thesauri/>
prefix xyz:  <http://sparql.xyz/facade-x/data/>
prefix fx:   <http://sparql.xyz/facade-x/ns/>
prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>

construct {
  $_thes_iri skos:member ?item.
  ?item a skos:Concept; skos:notation ?code; skos:prefLabel ?label.
}
where { service <x-sparql-anything:>
  { fx:properties fx:location $_location.
    [] a xyz:Row;
      rdf:_1 [xyz:ColumnRef "code"; rdf:_1/rdf:_1 ?code];
      rdf:_2 [xyz:ColumnRef "EN";   rdf:_1/rdf:_1 ?label]
  }
  bind(iri(concat(str($_thes_iri),"/",?code)) as ?item)
}
```
`$_thes_iri, $_location` are query params passed on the command line using `-v`.
So we have a `Makefile` with lines like this:
```
sparql-anything -v location=eBIZ-NT11.xml -o eBIZ-NT11.ttl -v thes=inventory/reason/transport -q eBiz.rq
```

See [sparql.anything#571](https://github.com/SPARQL-Anything/sparql.anything/issues/571) for a potential improvement: shorten the output by using `base`.
