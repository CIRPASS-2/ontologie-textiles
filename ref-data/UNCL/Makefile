.PHONY: all clean extract

JAR  := java -jar sparql-anything-v1.1.0.jar
COLL := doc/unece/refCodeListsTextile
MSG  := "The command has been commented out to avoid accidental overwrite since the TSV has been edited manually."

# (Warn on TSV extract, Build TTL)
STD_LIST := 1001 1229 1373 2379 3035 3055 3139 3227 4405 4451 4499 7187 7233 7491 8053

# (Custom echo on TSV extract, No TTL build)
INFO_LIST := 3207 3453 3499

all: $(patsubst %,UNCL%.ttl,$(STD_LIST))

clean: ; rm -f *.ttl

extract: $(patsubst %,UNCL%.tsv,$(STD_LIST) $(INFO_LIST))

%.ttl: %.tsv uncl_convert.rq
	$(JAR) -v location=$< -o $@ -v parent=$(PARENT) -v collection=$(COLL) -q uncl_convert.rq

UNCL1001.ttl: PARENT = thesauri/document/document
UNCL1229.ttl: PARENT = thesauri/trade_action
UNCL1373.ttl: PARENT = thesauri/document/status
UNCL2379.ttl: PARENT = thesauri/date_time_format
UNCL3035.ttl: PARENT = thesauri/party_function
UNCL3055.ttl: PARENT = thesauri/code_list_responsible_agency
UNCL3139.ttl: PARENT = thesauri/contact_function
UNCL3227.ttl: PARENT = thesauri/location/function
UNCL4405.ttl: PARENT = thesauri/status/status
UNCL4451.ttl: PARENT = thesauri/note_subject
UNCL4499.ttl: PARENT = thesauri/inventory/movement_reason
UNCL7187.ttl: PARENT = thesauri/process/process
UNCL7233.ttl: PARENT = thesauri/package/marking
UNCL7491.ttl: PARENT = thesauri/inventory/inventory
UNCL8053.ttl: PARENT = thesauri/transport/equipment

$(patsubst %,UNCL%.tsv,$(STD_LIST)): ; @echo $(MSG)

UNCL3207.tsv: ; @echo "Use ISO 3166-1 two alpha country code. (3207 Country name code)"
UNCL3453.tsv: ; @echo "Use ISO 639-1 (3453 Language name code)"
UNCL3499.tsv: ; @echo "Use ISO 5218 Representation of human sexes (3499 Gender code)"