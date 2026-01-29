JAR_VER = sparql-anything-v1.1.0.jar
JAR_FILE := ../../bin/${JAR_VER}
echo:
	@echo targets: get, rdfize

rdfize:
	java -jar ${JAR_FILE} -v location=eBiz_NT11.xml -o eBiz_NT11.ttl -v thes=inventory/reason/transport -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT13.xml -o eBiz_NT13.ttl -v thes=thesauri/fabric/fault_category -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT26.xml -o eBiz_NT26.ttl -v thes=thesauri/color/color -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT31.xml -o eBiz_NT31.ttl -v thes=thesauri/product/yarn_category -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT32.xml -o eBiz_NT32.ttl -v thes=thesauri/product/fabric_category -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT38.xml -o eBiz_NT38.ttl -v thes=thesauri/color/test -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT41.xml -o eBiz_NT41.ttl -v thes=thesauri/textile_characteristic/garment_attributes -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT71.xml -o eBiz_NT71.ttl -v thes=thesauri/picture/resolution_type -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_NT72.xml -o eBiz_NT72.ttl -v thes=thesauri/picture/intended_use_codes -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T12.xml  -o eBiz_T12.ttl  -v thes=thesauri/fabric/fault_type  -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T13.xml  -o eBiz_T13.ttl  -v thes=thesauri/textile_characteristic/fabric_technical -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T14.xml  -o eBiz_T14.ttl  -v thes=thesauri/fastness/test -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T15.xml  -o eBiz_T15.ttl  -v thes=thesauri/textile_process/dye_print -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T16.xml  -o eBiz_T16.ttl  -v thes=thesauri/dye_material/dye_material -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T17.xml  -o eBiz_T17.ttl  -v thes=thesauri/textile_characteristic/weave -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T19.xml  -o eBiz_T19.ttl  -v thes=thesauri/product/fibre -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T20.xml  -o eBiz_T20.ttl  -v thes=thesauri/textile_process/darning -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T200.xml -o eBiz_T200.ttl -v thes=thesauri/textile_process/raw_material -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T201.xml -o eBiz_T201.ttl -v thes=thesauri/textile_process/yarn -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T202.xml -o eBiz_T202.ttl -v thes=thesauri/textile_process/fabric -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T205.xml -o eBiz_T205.ttl -v thes=thesauri/textile_process/knitting_clothing -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T22.xml  -o eBiz_T22.ttl  -v thes=thesauri/textile_characteristic/material -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T24.xml  -o eBiz_T24.ttl  -v thes=thesauri/textile_characteristic/yarn -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T261.xml -o eBiz_T261.ttl -v thes=thesauri/yarn/technology -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T262.xml -o eBiz_T262.ttl -v thes=thesauri/fabric/technology -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T264.xml -o eBiz_T264.ttl -v thes=thesauri/fabric/printing_technology -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T281.xml -o eBiz_T281.ttl -v thes=thesauri/yarn/operation_parameters -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T282.xml -o eBiz_T282.ttl -v thes=thesauri/fabric/operation_parameters -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T422.xml -o eBiz_T422.ttl -v thes=thesauri/market/segment -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T423.xml -o eBiz_T423.ttl -v thes=thesauri/textile_characteristic/value_base_system -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T44.xml  -o eBiz_T44.ttl  -v thes=thesauri/textile_characteristic/additional_attributes -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T45.xml  -o eBiz_T45.ttl  -v thes=thesauri/fabric/print_parameter -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T48.xml  -o eBiz_T48.ttl  -v thes=thesauri/textile_characteristic/apparel_section -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T49.xml  -o eBiz_T49.ttl  -v thes=thesauri/substance_of_concern/chemical -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T54.xml  -o eBiz_T54.ttl  -v thes=thesauri/yarn/yarn -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T56.xml  -o eBiz_T56.ttl  -v thes=thesauri/yarn/ply -q eBiz.rq
	java -jar ${JAR_FILE} -v location=eBiz_T58.xml  -o eBiz_T58.ttl  -v thes=thesauri/yarn/quality_parameters -q eBiz.rq

get:
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT11.xml -o eBiz_NT11.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT13.xml -o eBiz_NT13.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT26.xml -o eBiz_NT26.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT31.xml -o eBiz_NT31.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT32.xml -o eBiz_NT32.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT38.xml -o eBiz_NT38.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT41.xml -o eBiz_NT41.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT71.xml -o eBiz_NT71.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_NT72.xml -o eBiz_NT72.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T12.xml  -o eBiz_T12.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T13.xml  -o eBiz_T13.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T14.xml  -o eBiz_T14.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T15.xml  -o eBiz_T15.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T16.xml  -o eBiz_T16.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T17.xml  -o eBiz_T17.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T19.xml  -o eBiz_T19.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T20.xml  -o eBiz_T20.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T200.xml -o eBiz_T200.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T201.xml -o eBiz_T201.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T202.xml -o eBiz_T202.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T205.xml -o eBiz_T205.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T22.xml  -o eBiz_T22.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T24.xml  -o eBiz_T24.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T261.xml -o eBiz_T261.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T262.xml -o eBiz_T262.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T264.xml -o eBiz_T264.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T281.xml -o eBiz_T281.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T282.xml -o eBiz_T282.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T422.xml -o eBiz_T422.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T423.xml -o eBiz_T423.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T44.xml  -o eBiz_T44.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T45.xml  -o eBiz_T45.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T48.xml  -o eBiz_T48.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T49.xml  -o eBiz_T49.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T54.xml  -o eBiz_T54.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T56.xml  -o eBiz_T56.xml
# 	curl -s https://www.ebiz.enea.it/moda-ml/repository/codelist/v2018-1/gc_T58.xml  -o eBiz_T58.xml 

