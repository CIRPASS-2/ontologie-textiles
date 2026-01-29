JAR_VER = sparql-anything-v1.1.0.jar
JAR_FILE := ../../bin/${JAR_VER}

.PHONY: all clean install

all: skos.concepts.ttl

skos.concepts.ttl: taxonomy.concepts.ttl uncl.concepts.ttl hazards.concepts.ttl
	cat taxonomy.concepts.ttl uncl.concepts.ttl hazards.concepts.ttl > skos.concepts.ttl

uncl.concepts.ttl: ../UNCL/UNCL*.ttl
	cat ../UNCL/UNCL*.ttl  > uncl.concepts.ttl

hazards.concepts.ttl: ../hazard-pesticide/hazard-GHS.ttl
	cat ../hazard-pesticide/hazard-GHS.ttl > hazards.concepts.ttl

taxonomy.concepts.ttl: taxonomy.rq paths.csv data.csv
	java -jar $(JAR_FILE) -q taxonomy.rq -o $@

data.csv:
	curl -L "https://docs.google.com/spreadsheets/d/1kC1DnHEIsKaX39I31gkQyCJ4FqHbn9lDuZC3NEIP0mE/export?format=csv&gid=0" -o $@

paths.csv: data.csv
	@echo "thes_url" > $@
	@tail -n +2 $< | awk -F, '{ \
		path = $$1; \
		if (path != "") { \
			print path; \
			while (index(path, "/") > 0) { \
			sub("/[^/]*$$", "", path); \
			print path; \
			} \
		} \
	}' >> $@

install:
	curl -L "https://github.com/SPARQL-Anything/sparql.anything/releases/download/v1.1.0/$(JAR_VER)" -o $(JAR_FILE)

clean:
	rm -f paths.csv data.csv taxonomy.concepts.ttl uncl.concepts.ttl hazards.concepts.ttl
