# Independent review receipt

A read-only reviewer inspected the workflow builder, ledger, tests, Compose file and README. It reproduced two material validation issues: purchase-order prefixes could match longer order numbers, and required nullable fields could be absent. Both received failing regression tests before fixes, and both passed on recheck. Invalid source field types were also made safe. The reviewer independently ran the then-current 30-test suite successfully and reported no remaining material blocker for the local educational demo. Four additional evidence/API checks were subsequently added; the final suite has 34 tests.

The CSV export now includes the extracted business fields. The README and presentation notes disclose that quote matching does not prove semantic support and that the model uses the Qwen Research License.

The final CPU image, PDF export and package received local verification after the independent review. Those artifact checks are documented in VERIFICATION.md; they were not represented as an additional independent security audit.
