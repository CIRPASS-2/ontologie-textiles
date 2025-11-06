This is initial work on a DPP for Textiles by GS1 and Graphwise.

## Reference Data

For now we're collecting some [ref-data](ref-data):
- Taxonomies
- Large nomenclatures like EU CN and WCO HS (tariff codes), ECHA EC and CAS (chemicals), UN-LOCODE (places)
- Sustainability standards from [StandardsMap](https://www.standardsmap.org/)

Important: Github has a limit of 50Mb per file, so if you have some large files do this:
- For intermediate files that don't need to be shared with others because they can be reproduced:
  add them to .gitignore
- For final files that need to be shared eg because they need to be loaded in a semantic repo:
  use [git lfs](https://git-lfs.com/):
```
git lfs install
You only need to run this once per user account.
git lfs track <my-large-file>
```

Then use commit and push as for normal files.

## Ontologies
[Ontology](ontology) work is just starting
