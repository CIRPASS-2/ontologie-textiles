JAR_VER = sparql-anything-v1.1.0.jar
JAR_FILE := ../../bin/${JAR_VER}

.PHONY: all clean install

all: hazard-GHS.ttl

hazard-GHS.ttl: hazard-GHS.rq hazard-GHS.tsv
	java -jar ${JAR_FILE} -v collection=doc/wikipedia/ghs -q hazard-GHS.rq -o $@

clean:
	rm hazard-GHS.ttl

install:
	curl -L "https://github.com/SPARQL-Anything/sparql.anything/releases/download/v1.1.0/$(JAR_VER)" -o $(JAR_FILE)

