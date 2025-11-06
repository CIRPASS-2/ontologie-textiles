<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Ontology Reviews](#ontology-reviews)
- [MVP](#mvp)

<!-- markdown-toc end -->

# Ontology Reviews
We have reviewed comprehensively 2 relevant ontologies:
- [UNTP Ontology Review](https://docs.google.com/document/d/1R3yqaYCO3JTpWsIckSzbumzyQgwRvd5X4Ewg-9Ax4yU/edit) (United Nations Transparency Protocol)
  - Issues posted on the [UNTP gitlab at UNICC](https://opensource.unicc.org/un/unece/uncefact/spec-untp/-/issues)
  - [Ontologies saved as turtle](https://github.com/VladimirAlexiev/untp-ontologies) at github 
- [Cirpass2 Ontology Review: Core and Substances of Concern](https://docs.google.com/document/d/1yGp35EHM_54bdIllKz_iXvdFDFs7ahfm9OOcXjZDUWc/edit)

The full bibliographic records are below:
```bibtex
@TechReport{AlexievEtAl-Cirpass2-Review-2025,
  author       = {Vladimir Alexiev and Elio Hbeich and Robert David},
  title        = {UNTP Ontology Review},
  institution  = {Graphwise and GS1},
  year         = 2025,
  month        = {oct},
  url          = {https://docs.google.com/document/d/1R3yqaYCO3JTpWsIckSzbumzyQgwRvd5X4Ewg-9Ax4yU/edit},
  keywords     = {DPP, ontology, ontology review, semantic modeling, UNTP},
  date         = {2025-10-23},
  abstract     = {The document is a review of the United Nations Transparency Protocol (UNTP) ontologies, identifying problems and areas for improvement. Purpose: The review aims to help the EU Cirpass2 project assess UNTP ontology suitability; and to facilitate posting issues to UNTP (at UNICC GitLab). Parts: Describes the current UNTP domains (core, dcc, dfr, dia, dpp, dte). Links to a github repo with Turtle variants and some analysis. Outlines issues in 16 detailed subsections. After general approval at the UNTP mailing list, all the issues were posted on the UNTP gitlab},
}

@TechReport{AlexievEtAl-Cirpass2-Review-2025,
  author       = {Vladimir Alexiev and Elio Hbeich and Ivo Ladenius},
  title        = {Cirpass2 Ontology Review: Core and Substances of Concern},
  institution  = {Graphwise and GS1},
  year         = 2025,
  month        = {oct},
  url          = {https://docs.google.com/document/d/1yGp35EHM_54bdIllKz_iXvdFDFs7ahfm9OOcXjZDUWc/edit},
  keywords     = {Cirpass, Cirpass2, DPP, ontology, ontology review, semantic modeling, UNTP},
  date         = {2025-10-23},
  abstract     = {This document is a review of the Cirpass2 core ontology, which is the first iteration of the EU Digital Product Passport (DPP) core ontology proposal. The review highlights several issues, including: Lack of reuse of UNTP ontologies: The document suggests that reusing UNTP ontologies would save development time and broaden the global reach of Cirpass DPP ontologies. Namespace and Naming problems: Issues such as using http instead of https for namespaces, non-permanent URLs, inconsistent spelling, and poorly named classes and properties. Ontology Metadata issues: Problems with author representation, empty contributor values, and comments attached to blank nodes. Modularity Errors: The core ontology is formed by concatenating modules, leading to redundant metadata and version information. The reviewer suggests using owl:import and potentially a single namespace for better modularity. Syntax Errors and Typos: Examples include mistyped ontology URLs and spelling mistakes. Description Errors: Comments with incorrect language tags, unclosed parentheses, misspellings, poor line breaks, and imprecise or misleading descriptions. It also suggests moving source information to dc:source and links to rdfs:seeAlso. Descriptive Omissions: Many terms lack rdfs:label and rdfs:comment, making them unclear. External Property Errors: Misspelling of skos:exactMatch and improper redefinition of owl:topDataProperty. Modeling Problems and Omissions: Issues with rdfs:subPropertyOf owl:topObjectProperty declarations, unelaborated dimensions and quality indicators, role modeling problems, missing links for permissions, no relation to Verifiable Credentials, inverse property naming, and failure to reuse GS1 Digital Link types. QuantitativeProductProperty Modeling Problems: These properties are often not elaborated, and there's a need for a more flexible way to capture what is being measured. It also points out that QuantityValue lacks defined MeasurementUnit and QuantityKind, suggesting the use of QUDT classes. Identifiers Not Modeled Adequately: Inconsistent ID property ranges and a lack of clear structure for identifier schemes. Recommendations include using adms:Identifier and considering W3C DIDs and/or GS1 identifiers. Unwarranted Union Datatypes: The use of union datatypes for uniqueProductID and webLink is considered unwarranted. Undefined classes and properties: The ontology includes undefined classes and properties like Type, hasType, and participatesInEvent. Duplication of annotation properties: Due to merging modules, standard annotation properties are defined multiple times.},
}
```

# MVP
A [MVP Textile DPP](https://dpp.vocabulary-hub.eu/message-model-tree/Message_0e9f0257-c021-48fb-bad5-fe15791d8e66?panes=element_tree:Message_0e9f0257-c021-48fb-bad5-fe15791d8e66:hkz1hp:primary) was proposed recently at the [CIRPASS-2 Digital Product Passport Vocabulary Hub](https://dpp.vocabulary-hub.eu/)
