# Issue 16: Common and Connector integration

Textile Common (`https://w3id.org/eudpp/textile-common`) is the canonical shared
module. The historical namespace `https://w3id.org/eudpp/textile-connector#`
and prefix `txtcon` are retained for all 37 terms. The separate Connector
compatibility graph contains every non-header Common triple, including 33
supporting triples, and has its own ontology header and SI import. It does not
import Common. Do not load the two representations as distinct sources in a
context that requires only one identity without considering the duplicated axioms.

The package identity is `integration-2026-11.2`; it is an unpublished internal
snapshot and does not decide the next release. Retained modules and Connector
record their `.1` predecessor. Common is a new identity and records the old
Connector as a migration predecessor with `dcterms:replaces`, rather than
claiming a Common 2.0.0. The quantitative shape succeeds its own 2.0.0 identity.
Historical 2.0.0 and `.1` packages use their own isolated catalogues; neither
is mapped to the changed `.2` graphs. Public HTTP dereferencing is not verified.

Reference periods preserve two boundaries, one boundary plus duration, and
duration alone. Approved positive durations use SI second, minute, hour or day;
quantity kind, when present, is time. Boundary comparison requires consistent
timezone representation. No calendar arithmetic or automatic consistency check
between a duration and boundaries is asserted. The fraction
`RangeThresholdValue` scalar-presence limitation remains deferred.

The approved issue #16 source is `b05927c3e32ff0d0b82ce6d5a55dc60665f9168f`.
The source's import-only Connector and term-subject-only candidate are superseded
by the owner-approved complete import-free representation. Issues #9 and #12
remain part of the ordered cumulative proof; the issue #12 decision record is
preserved byte-for-byte. CORE and all MIREOT source snapshots are unchanged.
