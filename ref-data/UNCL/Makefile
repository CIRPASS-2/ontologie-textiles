.PHONY: extract convert clean

extract: UNCL1001.tsv UNCL1229.tsv UNCL1373.tsv UNCL2379.tsv UNCL3035.tsv UNCL3055.tsv UNCL3139.tsv UNCL3227.tsv UNCL3453.tsv UNCL3499.tsv UNCL4405.tsv UNCL4451.tsv UNCL4499.tsv UNCL7187.tsv UNCL7233.tsv UNCL7491.tsv UNCL8053.tsv

UNCL1001.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred1001.htm > $@

UNCL1229.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred1229.htm > $@

UNCL1373.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred1373.htm > $@

UNCL2379.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred2379.htm > $@

UNCL3035.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3035.htm > $@

UNCL3055.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3055.htm > $@

UNCL3139.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3139.htm > $@
	# ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3207.htm # not a real thesaurus, says "Refer to ISO"

UNCL3227.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3227.htm > $@

UNCL3453.tsv:
	# ./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3453.htm > $@

UNCL3499.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred3499.htm > $@

UNCL4405.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4405.htm > $@

UNCL4451.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4451.htm > $@

UNCL4499.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred4499.htm > $@

UNCL7187.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred7187.htm > $@

UNCL7233.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred7233.htm > $@

UNCL7491.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred7491.htm > $@

UNCL8053.tsv:
	./uncl_extract.sh run --url https://service.unece.org/trade/untdid/d22a/tred/tred8053.htm > $@

convert:
	sparql-anything -v location=UNCL1001.tsv -o UNCL1001.ttl -v thes=thesauri/inventory -q uncl_convert.rq
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

clean:
	rm -rf venv/
