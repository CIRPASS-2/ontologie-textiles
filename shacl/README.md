# SHACL application profiles

The three default structural profiles cover shared quantities, recyclability
and Textile SoC. Merge the documented offline ontology closure with instance
data, use RDFS inference and disable remote imports. The validator performs
this merge explicitly. Recyclability retains its RDFS entailment declaration.
No profile requires OWL entailment during validation.

The SoC profile targets positive presences, qualification identity/context/source,
structured references, locations, denominator membership, concentration branches,
threshold expressions/evaluations and instruction text. It is a decimal mass-fraction
profile: approved unit IRIs are `units:one` and CORE `massFractionUnit`; values
remain ratios in [0,1]. Arbitrary or temperature units fail an IRI whitelist even
if domain/range inference gives them MeasurementUnit typing. Other quantity/unit
conventions require a separate justified profile, not numeric rescaling here.

Concentration is optional on partial presences. Add
`profiles/textile-soc-complete-report.ttl` explicitly to require it. The default
loader uses only top-level shape files. Use `--full --complete-report` to select
that additional profile in the public validator. Completeness here means the
additional concentration relationship, not ontology-wide regulatory completeness.

Named property and SPARQL constraint resources give stable result identities.
The matcher also resolves older anonymous property shapes by their actual named
container and path, and matches focus, component, path, severity and optional
message/source-constraint identity one-to-one. Forty-one migration scenarios retain
exact result multisets. Every targeted SoC shape has positive focus coverage
and discriminating negative coverage. The existing sixteen SHACL regression
scenarios and recyclability inference control remain unchanged in purpose.

## Reference duration and interval validation (issue #16)

The default profile retains both endpoints, one endpoint and duration, and
duration alone. Duration alone is an unanchored extent and does not identify
a calendar interval. Endpoints, when comparable, must be strictly ordered;
incomparable date-times are rejected. Date-times without offsets do not provide
an unambiguous global instant. The profile does not derive endpoints, check
duration consistency with endpoints, or implement calendar arithmetic.

A reference duration must have a positive decimal scalar and one supported
time unit. The current offline profile accepts SI Reference Point identifiers
`units:second`, `units:minute`, `units:hour`, and `units:day`. Second is an SI
base unit; minute, hour and day are non-SI units accepted for use with SI.
The selected SI MIREOT already declares minute and day. Second and hour are explicitly accepted
based on the authoritative SI Reference Point, not inferred from unit labels:
https://si-digital-framework.org/SI/units/second and
https://si-digital-framework.org/SI/units/hour. This bounded exchange profile
does not claim these are the only temporal units. Other valid time units,
prefixed or structured unit expressions, and calendar months/years require a
separately reviewed profile extension with authoritative dimensional evidence.
Unknown identifiers, literals and blank-node units fail this duration profile.
Existing data using a different time unit needs a reviewed mapping or extension;
it is not automatically converted. A `day` is an elapsed SI-compatible unit,
not a calendar-day or daylight-saving arithmetic convention.

When `txtcon:hasQuantityKind` is supplied on a reference duration, the default
profile requires the SI Reference Point time quantity kind
`https://si-digital-framework.org/quantities/TIME`. It remains optional. A
different quantity kind, including length, is rejected even if the unit is a
time unit. The TIME individual is already present in the selected SI MIREOT.
