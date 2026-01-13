JAR_FILE := sparql-anything-v1.1.0.jar
CSV_FILE := data.csv
PATHS_FILE := paths.csv
RESULT_FILE := taxonomy.concepts.ttl

# Default target
all: $(JAR_FILE) fetch urls transform

# Download the file only if it does not exist
$(JAR_FILE):
	curl -L "https://github.com/SPARQL-Anything/sparql.anything/releases/download/v1.1.0/$(JAR_FILE)" -o $(JAR_FILE)

fetch:
	curl -L "https://docs.google.com/spreadsheets/d/1kC1DnHEIsKaX39I31gkQyCJ4FqHbn9lDuZC3NEIP0mE/export?format=csv&gid=0" -o $(CSV_FILE)

urls:
	@echo "Processing $(CSV_FILE) (skipping header)..."
	@tail -n +1 $(CSV_FILE) | while IFS= read -r line; do \
	    col=$$(echo "$$line" | cut -d',' -f1); \
	    while [ -n "$$col" ]; do \
	        echo "$$col" >> $(PATHS_FILE); \
	        if echo "$$col" | grep -q "/"; then \
	            col=$${col%/*}; \
	        else \
	            break; \
	        fi; \
	    done; \
	done
	@echo "Done. All paths written to $(PATHS_FILE)"

transform:
	java -jar sparql-anything-v1.1.0.jar -q taxonomy.rq -o $(RESULT_FILE)
	@echo "Done. Taxonomy written to $(RESULT_FILE)"

clean:
	rm $(JAR_FILE) $(CSV_FILE) $(PATHS_FILE) $(RESULT_FILE)