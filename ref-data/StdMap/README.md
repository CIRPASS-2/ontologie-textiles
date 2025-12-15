# Standards Map Extraction

Standards Map is 

> The world’s largest database for sustainability standards

In this directory we have put various tools to extract them in a structured
format.

There are two undocumented public API endpoints:

  1. https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION
  2. https://api.production.standardsmap.sustainable-trade.org/api/standards/<ID>/all?preview=false

The first one has no arguments. In the second <ID> has to be replaced with
standard ID, for example 496 or 100000. The first one returns info on all
standards, the second one returns detailed information about a particular
standard.

## Further info on endpoints

### Endpoint 1

We pull and clean the info from endpoint 1. We use the R script `get-stdmap.R`
to do so. To run the R script, besides the R environment, you need to install
some libraries, which you can do by running `setup.R`. After the execution,
the following files are generated:

  - `a.JSON` is the JSON that is returned from the endpoint;
  we pretty-print it and "unbox" it, i.e. vectors of length 1 are represented
  as JSON scalars.
  - `a.csv` is a summary of the standards in tabular format; the 
  fields that we keep areall except `themeScores`, some
  elements are renamed 
  
We do some data-cleaning:

  - remove `\n`
  - extract URLs 
  - format dates
  - etc
### Endpoint 2

For now (2025-10-28), we are not using this endpoint.

## Files and directory structure

### `manual`

```
csvtk cut -f origin      StdMap-Standard.csv|perl -pe 's{;}{\n}g'|sort|uniq>country-origin.txt
csvtk cut -f destination StdMap-Standard.csv|perl -pe 's{;}{\n}g'|sort|uniq>country-destination.txt
csvtk cut -f mandate     StdMap-Standard.csv|perl -pe 's{;}{\n}g'|sort|uniq -c|sort -rn>mandate.txt
```

### thes

Thesauri. Files are created here with the R scripts in the R directory and then
further manually processed in Google docs: run `get-thesauri-and-concepts.R`:
this will create two files that are further manually processed in Google docs.

### root

The main action is here.