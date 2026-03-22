import unittest

from orchestrator.contracts import ContractViolationError, validate_agent_response


class ContractValidationTests(unittest.TestCase):
    def test_planner_missing_key_fails(self):
        with self.assertRaises(ContractViolationError):
            validate_agent_response("planner", {"tasks": [{"task_id": "1", "title": "t"}]})

    def test_critic_invalid_verdict_fails(self):
        with self.assertRaises(ContractViolationError):
            validate_agent_response(
                "critic",
                {
                    "verdict": "unknown",
                    "scores": {},
                    "reasons": [],
                    "repair_instructions": [],
                },
            )

    def test_qa_valid_payload_passes(self):
        validate_agent_response("qa", {"verdict": "pass", "notes": ["ok"]})


if __name__ == "__main__":
    unittest.main()
