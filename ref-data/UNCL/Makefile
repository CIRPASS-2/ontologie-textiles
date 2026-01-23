.PHONY: extract convert clean

extract: UNCL1001.tsv UNCL1229.tsv UNCL1373.tsv UNCL2379.tsv UNCL3035.tsv UNCL3055.tsv UNCL3139.tsv UNCL3227.tsv UNCL3453.tsv UNCL3499.tsv UNCL4405.tsv UNCL4451.tsv UNCL4499.tsv UNCL7187.tsv UNCL7233.tsv UNCL7491.tsv UNCL8053.tsv

UNCL1001.tsv:
	echo "The command has been commented out to avoid accidental overwrite since the TSV has been edited manually."
    #./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred1001.htm > $@ # 1001 Document name code

UNCL1001.ttl: UNCL1001.tsv uncl_convert.rq
	java -jar sparql-anything-v1.1.0.jar -v location=UNCL1001.tsv -o UNCL1001.ttl -v parent=thesauri/document -v title="Document type" -v collection=doc/unece/refCodeListsTextile -q uncl_convert.rq

UNCL1229.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred1229.htm > $@ # 1229 Action request/notification description code

UNCL1373.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred1373.htm > $@ # 1373 Document status code

UNCL2379.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred2379.htm > $@ # 2379 Date or time or period format code

UNCL3035.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3035.htm > $@ # 3035 Party function code qualifier

UNCL3055.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3055.htm > $@ # 3055 Code list responsible agency code

UNCL3139.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3139.htm > $@ # 3139 Contact function code

UNCL3207.tsv:
    # ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3207.htm # Use ISO 3166-1 two alpha country code. (3207 Country name code)

UNCL3227.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3227.htm > $@ # 3227 Location function code qualifier

UNCL3453.tsv:
    #./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3453.htm > $@ # Use ISO 639-1 (3453 Language name code)

UNCL3499.tsv:
    # ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3499.htm > $@ #  1 Use ISO 5218 Representation of human sexes (3499 Gender code)

UNCL4405.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4405.htm > $@ # 4405 Status description code

UNCL4451.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4451.htm > $@ # 4451 Text subject code qualifier

UNCL4499.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4499.htm > $@ # 4499 Inventory movement reason code

UNCL7187.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred7187.htm > $@ # 7187 Process type description code

UNCL7233.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred7233.htm > $@ # 7233 Packaging related description code

UNCL7491.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred7491.htm > $@ # 7491 Inventory type code

UNCL8053.tsv:
    ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred8053.htm > $@ # 8053 Equipment type code qualifier


convert:
	sparql-anything -v location=UNCL1229.tsv -o UNCL1229.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL1373.tsv -o UNCL1373.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL2379.tsv -o UNCL2379.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL3035.tsv -o UNCL3035.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL3055.tsv -o UNCL3055.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL3139.tsv -o UNCL3139.ttl -v thes=TODO/TODO -q uncl_convert.rq
	# sparql-anything -v location=UNCL3207.tsv -o UNCL3207.ttl -v thes=TODO/TODO -q uncl_convert.rq # not a real thesaurus
	sparql-anything -v location=UNCL3227.tsv -o UNCL3227.ttl -v thes=TODO/TODO -q uncl_convert.rq
	# sparql-anything -v location=UNCL3453.tsv -o UNCL3453.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL3499.tsv -o UNCL3499.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL4405.tsv -o UNCL4405.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL4451.tsv -o UNCL4451.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL4499.tsv -o UNCL4499.ttl -v thes=inventory/reason/movement -q uncl_convert.rq
	sparql-anything -v location=UNCL7187.tsv -o UNCL7187.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL7233.tsv -o UNCL7233.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL7491.tsv -o UNCL7491.ttl -v thes=TODO/TODO -q uncl_convert.rq
	sparql-anything -v location=UNCL8053.tsv -o UNCL8053.ttl -v thes=TODO/TODO -q uncl_convert.rq

