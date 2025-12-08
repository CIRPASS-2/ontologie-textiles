# StandardsMap Extraction

There are two undocumented public API endpoints:

  1. https://api.production.standardsmap.sustainable-trade.org/api/standards?client=NO%20AFFILIATION
  2. https://api.production.standardsmap.sustainable-trade.org/api/standards/<ID>/all?preview=false

The first one has no arguments. In the second <ID> has to be replaced with
standard ID, for example 496 or 100000. The first one returns info on all
standards, the second one returns detailed information about a particular
standard.

## What we do

### Endpoint 1

We pull and clean the info from endpoint 1. We use the R script `get-stdmap.R`
to do so. To run the R script, besides the R environment, you need to install
some libraries, which you can do by running `setup.R`. After the execution,
the following files are generated:

  - `StdMap-Extraction.JSON` is the JSON that is returned from the endpoint;
  we pretty-print it and "unbox" it, i.e. vectors of length 1 are represented
  as JSON scalars.
  - `StdMap-Standard.csv` is a summary of the standards in tabular format; the 
  fields that we keep are
    - `url`
    - `standard`
    - `sectors`
    - `products`
    - `weblink`
    - `descr`
  - `StdMap-Standard-Extended.csv` has the same rows, but more elements from
  the JSON are converted into tabular format (all except `themeScores`, some
  elements are renamed)
  
We do some data-cleaning:

  - remove `\n`
  - extract URLs 
  - format dates
  - etc
  
### Endpoint 2

For now (2025-10-28), we are not using this endpoint.

## Thesauri and concepts extraction

TODO document this