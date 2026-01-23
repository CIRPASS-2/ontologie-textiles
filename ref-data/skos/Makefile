JAR_FILE := sparql-anything-v1.1.0.jar

.PHONY: all clean full-clean

all: taxonomy.concepts.ttl uncl.concepts.ttl

uncl.concepts.ttl: ../UNCL/UNCL1001.ttl
	cat ../UNCL/UNCL1001.ttl > uncl.concepts.ttl

taxonomy.concepts.ttl: taxonomy.rq paths.csv data.csv $(JAR_FILE)
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

$(JAR_FILE):
	curl -L "https://github.com/SPARQL-Anything/sparql.anything/releases/download/v1.1.0/$(JAR_FILE)" -o $@

clean:
	rm -f paths.csv data.csv $(JAR_FILE)

full-clean:
	rm -f $(JAR_FILE) paths.csv data.csv taxonomy.concepts.ttl
