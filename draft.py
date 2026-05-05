Step 1 — Find DomCo cases with SCAP-1
grep -rl "Domiciliary Company" OUTPUT_FOLDER/*/*/edd_text_parser.json | \
  xargs grep -l "SCAP-1"
This gives you all cases that are DomCo + sensitive country — candidates for Scenario 1 or 2.

Step 2 — Among those, check BO SCAP results
# Find cases where NO BO has SCAP-1 active → Scenario 1
grep -rL "SCAP1 Compliance: Active" OUTPUT_FOLDER/<case_number>/*/kyc_checks_output.json

# Find cases where AT LEAST ONE BO has SCAP-1 active → Scenario 2
grep -rl "SCAP1 Compliance: Active" OUTPUT_FOLDER/<case_number>/*/kyc_checks_output.json
Step 3 — Find non-DomCo cases → Scenario 3
grep -rl "Operating Company\|Trust\|Individual" OUTPUT_FOLDER/*/*/edd_text_parser.json
Verify the exclusion fired (Scenario 1)
Once you have a candidate case, check the DomCo's own kyc_checks_output.json:

grep -r "SCAP-1 excluded" OUTPUT_FOLDER/<case_number>/
If it's there — exclusion fired. If not — SCAPGraph ran instead.
