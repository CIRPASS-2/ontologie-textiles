CPP := gcc-15
CPP_FLAGS := -E -P -C -nostdinc -Wno-invalid-token-paste
CHUNK_DIR := .chunks

all: rdf/stdmap.ttl

prefixes.rq: prefixes.ttl
	perl -pe 'm{###} and last; s{^@}{}; s{ *\.$$}{}' $^ > $@

%.png: %.ttl
	perl -S rdfpuml.pl $*.ttl
	plantuml $*.puml
	rm $*.puml

stdmap.tarql: model-origin.tarql model-dest.tarql model-meta.tarql model-products.tarql
	cat $^ > $@

%.tarql: prefixes.rq macros.h %.ttl 
	mkdir -p $(CHUNK_DIR)/$*
	gcsplit -s -f $(CHUNK_DIR)/$*/ -b "%02d.part" $*.ttl "/###/" "{*}"
	rm -f $@.temp
	for f in $(CHUNK_DIR)/$*/*.part; do \
		sed -i '' '/###/d' $$f; \
		perl -S rdf2sparql.pl -tarql $$f | \
		cat macros.h prefixes.rq - | \
		$(CPP) $(CPP_FLAGS) - >> $@.tmp; \
	done

	mv $@.tmp $@
	rm -rf $(CHUNK_DIR)/$*

rdf/stdmap.ttl: stdmap.tarql data/stdmap.csv
	tarql --base https://w3id.org/eudpp/ --write-base $^ > temp.ttl; owl write --useCommaByDefault temp.ttl $@; rm temp.ttl

.PHONY clean:
	rm -f *.tarql
	rmdir .chunks