all: stdmap.ttl

prefixes.rq: prefixes.ttl
	perl -pe 'm{###} and last; s{^@}{}; s{ *\.$$}{}' $^ > $@

stdmap-model.tarql: prefixes.rq stdmap-model.ttl macros/common.h
	perl -S rdf2sparql.pl -tarql stdmap-model.ttl | cat macros/common.h prefixes.rq - | gcc-15 -E -P -C -nostdinc -Wno-invalid-token-paste - > $@

stdmap.ttl: stdmap-model.tarql stdmap.csv
	tarql --base https://w3id.org/eudpp/ --write-base $^ > temp.ttl; owl write --useCommaByDefault temp.ttl $@; rm temp.ttl

