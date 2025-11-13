all: hazard-GHS.ttl

hazard-GHS.ttl: hazard-GHS.rq | hazard-GHS.tsv
	sparql-anything -o $@ -q $^
