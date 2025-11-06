all: UNLOCODE-CodeList.ttl SubdivisionCodes.ttl

%.ttl: %.rq %.csv
	tarql -encoding latin1 --no-header-row --dedup 500 --base https://w3id.org/eudpp/ --write-base $^ > $@
