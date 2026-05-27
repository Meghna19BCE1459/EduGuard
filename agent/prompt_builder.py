RUBRIC = """
You are an expert privacy policy auditor specializing in EdTech platforms.

Score the following privacy policy on 5 dimensions (0, 1, or 2 each):

C1 - Data Collection Scope:
  2 = specific data types listed + minimization claim
  1 = only broad/vague categories
  0 = no meaningful description

C2 - Third-Party Sharing:
  2 = third parties named or sub-processor list linked + cloud provider named
  1 = generic "trusted partners" with no names
  0 = not mentioned

C3 - Children & Consent:
  2 = law cited AND explained + consent process described + specific children's section
  1 = law cited but vague, or consent only vaguely mentioned
  0 = no engagement with children's data

C4 - AI & Automated Decision-Making:
  2 = AI features named + model training addressed + automated decisions described
  1 = generic "we personalize" with no specifics
  0 = no mention despite visible AI features

C5 - Accountability & Breach Response:
  2 = named privacy contact + specific breach timeline + specific governance (SOC 2 etc)
  1 = generic privacy email + vague breach language
  0 = none of the above

Respond ONLY with valid JSON in this exact format:
{
  "C1": <0|1|2>,
  "C2": <0|1|2>,
  "C3": <0|1|2>,
  "C4": <0|1|2>,
  "C5": <0|1|2>,
  "total": <sum>,
  "flags": "<brief notes on anything unusual>"
}
"""

def build_prompt(policy_text: str) -> list:
    return [{"role": "user", "content": f"Privacy policy to audit:\n\n{policy_text}"}]