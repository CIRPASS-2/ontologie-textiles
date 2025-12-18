CPP := gcc-15
CPP_FLAGS := -E -P -C -nostdinc -Wno-invalid-token-paste

all: stdmap.ttl

prefixes.rq: prefixes.ttl
	perl -pe 'm{###} and last; s{^@}{}; s{ *\.$$}{}' $^ > $@

%.png: %.ttl
	perl -S rdfpuml.pl $*.ttl
	plantuml $*.puml
	rm $*.puml

stdmap.tarql: model-origin.tarql model-dest.tarql model-meta.tarql model-products.tarql
	cat $^ > $@

%.tarql: prefixes.rq macros.h %.ttl 
	perl -S rdf2sparql.pl -tarql $*.ttl | \
	cat macros.h prefixes.rq - | \
	$(CPP) $(CPP_FLAGS) - > $@

stdmap.ttl: stdmap.tarql stdmap.csv
	tarql --base https://w3id.org/eudpp/ --write-base $^ > temp.ttl; owl write --useCommaByDefault temp.ttl $@; rm temp.ttl

