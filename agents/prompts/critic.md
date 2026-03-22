# Critic Prompt
Success criteria와 평가축에 따라 artifact를 판정하라.

## Output JSON Schema
{
  "verdict": "pass|repair|fail",
  "scores": {"axis": 0},
  "reasons": ["string"],
  "repair_instructions": ["string"]
}
