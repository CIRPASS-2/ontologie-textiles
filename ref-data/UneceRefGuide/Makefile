all: unece-202104-v1.5-tidy.htm unece-202209-v1.2-tidy.htm unece-202104-v1.5-links.txt unece-202209-v1.2-links.txt

%-tidy.htm: %.htm
	-tidy --word-2000 1 --input-encoding latin1 -clean -bare -quiet --wrap 0 -f $*-errors.txt $^ > $@

%-links.txt: %-tidy.htm
	perl taxonomy-links.pl $^ > $@
	sort $*-links.txt | uniq -c > $*-links-sorted.txt

count:
	wc *.htm
	grep -Pic '>code list( #\d+)?<' unece-*-tidy.htm
	grep -Pic '>code tag<'          unece-*-tidy.htm
	grep -Pic '>code (value|name)<' unece-*-tidy.htm

count-links:
	wc -l *-links*.txt
	@echo 202104-v1.5; perl -nle 'print m{(\.[a-z]{1,4})$$} ? $$1 : ""' unece-202104-v1.5-links-sorted.txt|sort|uniq -c
	@echo 202209-v1.2; perl -nle 'print m{(\.[a-z]{1,4})$$} ? $$1 : ""' unece-202209-v1.2-links-sorted.txt|sort|uniq -c
