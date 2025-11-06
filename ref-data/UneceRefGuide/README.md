# Extracting Taxonomies from UNECE Guide
One of the key documents from the Cirpass scoping deliverable is the UNECE/UNCEFACT
**Recommendation on Code Lists and Identifiers for the Textile and Leather Sector**.
We parsed it out to extract all taxonomies.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Extracting Taxonomies from UNECE Guide](#extracting-taxonomies-from-unece-guide)
    - [Source](#source)
    - [HTML Tidy](#html-tidy)
    - [Picking a Version](#picking-a-version)
    - [Extacting and Counting Taxonomy Links](#extacting-and-counting-taxonomy-links)
    - [Automatically Processable Taxonomies](#automatically-processable-taxonomies)
    - [Diffing Links](#diffing-links)

<!-- markdown-toc end -->


## Source
It is available in several PDF versions:
- https://unece.org/sites/default/files/2021-05/TL_CodeLists-IdentifiersRecommendationv.pdf : dated 2021-05 in the URL, and 2022-10 on the title page.
- https://unece.org/sites/default/files/2023-10/Guidelines-ECE_TRADE_C_CEFACT_2022_INF1E.pdf : dated 2023-10 in the URL, and 2022-10 on the title page.

We were able to also find 3 Word `.docx` versions:
- 202103 v1.0
- 202104 v1.5
- 202209 v1.2

## HTML Tidy
There are now many capable libraries for parsing PDF, but there are complicating issues like page breaks, zoom levels and footnote marks.
So it is much easier to parse HTML.
This is how we proceeded:
- Open in Word and save as `Filtered HTML`: `unece-202104-v1.5.htm, unece-202209-v1.2.htm`
- This also saves two folders with images: `unece-202104-v1.5_files, unece-202209-v1.2_files`
- Rename the folders to `img-202104-v1.5, img-202209-v1.2`, and do a similar replacement inside the `.htm` files

Install HTML `tidy` from [tidy-html5/releases](https://github.com/htacg/tidy-html5/releases). This is a very capable software for cleaning up HTML.
See [General doc and tutorial](https://www.html-tidy.org/documentation/) and [Options Quick Reference](https://api.html-tidy.org/tidy/quickref_next.html)

Wrote a `Makefile` that runs it with the following options:
```
tidy --word-2000 1 --input-encoding latin1 -clean -bare -quiet --wrap 0 -f unece-202104-v1.5-errors.txt -o unece-202104-v1.5-tidy.htm unece-202104-v1.5.htm
tidy --word-2000 1 --input-encoding latin1 -clean -bare -quiet --wrap 0 -f unece-202209-v1.2-errors.txt -o unece-202209-v1.2-tidy.htm unece-202209-v1.2.htm
```
This makes parsing easier:
- Replaces smart quotes and non-breaking spaces with simple ASCII chars
- Omits line wrapping of the HTML source
- Cleans up empty spans and divs and superfluous styles

We can see that this leads to significant simplification:
```
wc *.htm
```
| lines | words |   chars | file                       |
|-------|-------|---------|----------------------------|
|  9506 | 20607 |  218272 | unece-202104-v1.5-tidy.htm |
| 19681 | 57995 | 1008456 | unece-202104-v1.5.htm      |
|  9108 | 20812 |  229697 | unece-202209-v1.2-tidy.htm |
| 19593 | 57355 | 1014695 | unece-202209-v1.2.htm      |

For example, UNCL 1229 that has footnote `[5]` looks like this in Word HTML:
```html
<p class="MsoNormal c4" align="center"><span lang="EN-GB" class=
'c72'>UNCL<a href="#_ftn5" name="_ftnref5" title="" id=
"_ftnref5"><span class=
"MsoFootnoteReference MsoFootnoteReference c74" lang=
"EN-GB">[5]</span></a> �1229</span></p>
```

And is cleaned up to this by tidy:
```html
<p align="center">UNCL<a href="#_ftn5" name="_ftnref5" title="" id="_ftnref5">[5]</a>  1229</p>
```

## Picking a Version
Which version of the two files should we use?
- v1.5 is a bigger  number but it's older (2021-04) and is smaller (218272 bytes)
- v1.2 is a smaller number but it's newer (2022-09) and is bigger (229697 bytes)

We decided to count the number of codelists in each of the versions:
```
$ grep -Pic '>code list( #\d+)?<' unece-*-tidy.htm
unece-202104-v1.5-tidy.htm:202
unece-202209-v1.2-tidy.htm:184

$ grep -Pic '>code tag<'          unece-*-tidy.htm
unece-202104-v1.5-tidy.htm:105
unece-202209-v1.2-tidy.htm:93

$ grep -Pic '>code (value|name)<' unece-*-tidy.htm
unece-202104-v1.5-tidy.htm:101
unece-202209-v1.2-tidy.htm:93
```

Notes:
- `make count` runs the `wc` and `grep` commands above
- `-Pic` means we use Perl regular expressions, case-insensitive, and only count
- `>...<` searches for the appearance of these words within a single HTML element (eg `<th` or `<b>`), not as part of a longer sentence
- First grep:
  - `code list` appears twice per codelist, so v1.5 has 101 and v1.2 has 92 codelists
  - v1.5 codelists are numbered, eg the last one is `Code List #101`, confirming the count. We use an optional regex `( #\d+)?`
- Second grep: `code tag` appears once per codelist
  - In v1.5 it also appears in `Glossary #1` to `Glossary #4`, that's why there are 4 more
  - In v1.2 it appears two extra times, we don't know why
- Third grep: the same numbers are confirmed

So it seems that version 1.5 is better for extracting taxonomies.
However:
- v1.2 has URLs in section `5 Details of identifiers`, 
  eg [OAR ID](https://info.openapparel.org/) (Open Apparel Registry ID for facility) and [GlobalGap GLN](https://certifications.controlunion.com/nl/certification-programs/certification-programs/globalgap),
  that are lacking in v1.2, so we'll use it for that purpose
- v1.2 refers to newer versions of UNCL codelists (see next section), eg
  - https://service.unece.org/trade/untdid/d22a/tred/tred1001.htm (in v1.2)
  - https://service.unece.org/trade/untdid/d20b/tred/tred1001.htm (in v1.5)

## Extacting and Counting Taxonomy Links

We wrote a very simple script `taxonomy-links.pl`:
```perl
#!perl -wn
1..m{Details of code lists</a></h1>} and next;
m{(Details of identifiers|Overview identifier schemes)</h1>} and last;
print "$1\n" while m{(http[^"]+)}g;
```
- It iterates over all lines
- Skips all lines until it sees section `4 Details of code lists`
- Quits if it sees section `5 Details of identifiers` (also called `5 Overview identifier schemes`)
- Prints all `http` and `https` links that it finds

We use it to extract these links, and also sort them (with count).
The Makefile does this:
```
perl taxonomy-links.pl unece-202104-v1.5-tidy.htm > unece-202104-v1.5-links.txt
sort unece-202104-v1.5-links.txt | uniq -c > unece-202104-v1.5-links-sorted.txt
perl taxonomy-links.pl unece-202209-v1.2-tidy.htm > unece-202209-v1.2-links.txt
sort unece-202209-v1.2-links.txt | uniq -c > unece-202209-v1.2-links-sorted.txt
```

Now let's count them:
```
wc -l *-links*.txt
   86 unece-202104-v1.5-links-sorted.txt
   96 unece-202104-v1.5-links.txt
  106 unece-202209-v1.2-links-sorted.txt
  192 unece-202209-v1.2-links.txt
```
- v1.5 has 86 unique links and v1.2 has 106 unique links
- Both versions have some link repetitions, but v1.2 has over 85 repetitions

If we inspect the repetitions:
```
grep -v ' 1 ' unece-202104-v1.5-links-sorted.txt | sort -rn
      4 https://www.sustainabilitymap.org/standards?q=eyJzZWxlY3RlZENsaWVudCI6Ik5PIEFGRklMSUFUSU9OIn0%3D
      4 https://textileexchange.org/wp-content/uploads/2020/09/ASR-213-V1.0-Materials-Processes-and-Products-Classification.pdf
      2 https://www.oecd-ilibrary.org/environment/oecd-guidelines-for-the-testing-of-chemicals-section-3-degradation-and-accumulation_2074577x
      2 https://unece.org/sites/default/files/2020-12/loc202csv.zip
      2 https://global-standard.org/images/resource-library/documents/standard-and-manual/gots_version_6_0_en1.pdf
      2 http://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2017-edition/hs-nomenclature-2017-edition.aspx
grep -v ' 1 ' unece-202209-v1.2-links-sorted.txt | sort -rn
     39 https://ebiz-tcf.eu/
     27 https://unece.org/trade/uncefact/mainstandards
      4 https://www.standardsmap.org/en/identify
      4 https://textileexchange.org/wp-content/uploads/2020/09/ASR-213-V1.0-Materials-Processes-and-Products-Classification.pdf
      4 https://textileexchange.org/
      4 https://intracen.org/
      3 https://www.oecd.org/
      3 https://www.iso.org/home.html
      3 http://www.iso.org/
      2 https://www.oecd-ilibrary.org/environment/oecd-guidelines-for-the-testing-of-chemicals-section-3-degradation-and-accumulation_2074577x
      2 https://www.globaltextilescheme.org/
      2 http://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2017-edition/hs-nomenclature-2017-edition.aspx
      2 http://www.wcoomd.org/
```
We see that
- v1.5 has a generic link for each taxonomy organization (`ebiz-tcf, unece, textileexchange, intracen` etc)
- Some of specific links are cited for more than one taxonomy, eg
  - https://textileexchange.org/wp-content/uploads/2020/09/ASR-213-V1.0-Materials-Processes-and-Products-Classification.pdf covers 4 taxonomies
  - http://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2017-edition/hs-nomenclature-2017-edition.aspx covers 2 taxonomies

## Automatically Processable Taxonomies

The most numerous taxonomies can be processed automatically:
- `eBiz` (Moda-ML eBiz schema) that are represented as Genericode XML and can be downloaded from URLs like
  - http://www.cross-tec.enea.it/moda-ml/repository/codelist/v2018-1/gc_T45.xml 
  - See folder [eBiz](../eBiz) for a `sparql-anywhere` script that extracts the info and makes SKOS turtle
  - Count:
```
grep -c .xml *links.txt
unece-202104-v1.5-links.txt:39
unece-202209-v1.2-links.txt:37
```
- `UNCL` (UNCEFACT codelists) that are represented as text wrapped in HTML and can be downloaded from URLs like
  - https://service.unece.org/trade/untdid/d22a/tred/tred1001.htm (in v1.2)
  - https://service.unece.org/trade/untdid/d20b/tred/tred1001.htm (in v1.5)
  - See folder [UNCL](../UNCL) for a Python script that  extracts the info
  - Count:
```
grep -c tred.*htm *links.txt
unece-202104-v1.5-links.txt:17
unece-202209-v1.2-links.txt:18
```

We also count links by filetype with commands like these (just use `make count-links`)
```
perl -nle 'print m{(\.[a-z]{1,3})$} ? $1 : ""' unece-202104-v1.5-links-sorted.txt
```

To summarize:

| links-sorted | unece-202104-v1.5 | unece-202209-v1.2 | comment                                  |
|--------------|-------------------|-------------------|------------------------------------------|
| eBiz=.xml    |                39 |                37 |                                          |
| UNCL=.htm    |                17 |                18 | 1.5 is older (d20b), 1.2 is newer (d22a) |
| .aspx        |                 1 |                 1 |                                          |
| .html        |                 2 |                 2 |                                          |
| .pdf         |                 3 |                 7 |                                          |
| .xls         |                 2 |                 3 |                                          |
| .xlsx        |                 2 |                 2 |                                          |
| .zip         |                 3 |                 2 |                                          |
| Other        |                17 |                34 |                                          |
| TOTAL        |                86 |               106 |                                          |
| Thesauri     |               101 |                92 |                                          |

- eBiz (`xml`) and UNCL (`htm`) links cna be processed automatically
- Other, `html` and `aspx` links are generic and need to be investigated separately (some of them are broken but can be found by googling)
- Some `xls` files can be processed but others (eg [BCI Pesticides-List-Classification](https://bettercotton.org/wp-content/uploads/2014/01/Guidance-Pesticides-List-Classification.xlsx)) are complex and require particular information design and processing
- `pdf` files are complex to process
  - We may only process Textile Exchange [ASR-213 Materials, Processes, & Products Classification](https://textileexchange.org/knowledge-center/documents/materials-processes-products-classification/) (here is [ASR-213-V1.4-2025.06.01](https://2d73cea0.delivery.rocketcdn.me/app/uploads/2024/05/ASR-213-V1.4-Materials-Processes-Products-Classification.pdf))
  - Others can be found in structured form, eg
  - UNECE Rec16 `LOCODE` [version 2012-12 as PDF](https://unece.org/sites/default/files/2020-12/ECE-TRADE-459E.pdf) can be found in newer versions as `csv, txt, mdb` [UNLOCODE-Download](https://unece.org/trade/cefact/UNLOCODE-Download)
- `zip` files include structured information:
  - Rec19 Transport Mode, with limited relevance for textile
  - GS1 GPC, which is a huge product classification with some attributes and values relevant to textile

For this phase of the project we'll process:
- eBiz (xml) and UNCL (htm)
- EU CN (one of the Other links) that is available as SKOS turtle from the EU Open Data Portal
- StandardsMap sustainability standards
- StandardsMap sustainability taxonomies (about 10)

## Diffing Links

TODO: compare unece-202104-v1.5-links.txt and unece-202209-v1.2-links.txt and comment on the differences

TODO: how come 1.5 has fewer thesaur but more links, and 1.2 is the opposite?
