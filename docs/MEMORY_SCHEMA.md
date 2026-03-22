# MEMORY_SCHEMA

## 디렉터리 구조

```text
memory/
  identity/
  policy/
  tasks/
    active/
    completed/
  knowledge/
    sources/
    summaries/
  decisions/
  failures/
  evaluations/
```

## 참조 우선순위
1. Constitution / policy
2. Active task context
3. Recent decisions
4. Current knowledge summaries
5. Failure lessons
6. Archived history

## 핵심 스키마

### GoalSpec
```yaml
project_id:
mission:
deliverables:
constraints:
success_criteria:
references:
budget_limits:
stop_conditions:
priority_order:
```

### TaskSpec
```yaml
task_id:
title:
description:
owner:
depends_on:
inputs:
expected_outputs:
status:
retry_count:
priority:
evaluation_refs:
```

### EvalSpec
```yaml
artifact_id:
reviewer:
verdict:
scores:
reasons:
repair_instructions:
risk_level:
timestamp:
```

### DecisionSpec
```yaml
decision_id:
context:
chosen_option:
rejected_options:
reasoning_summary:
revisit_conditions:
timestamp:
```

### FailureSpec
```yaml
failure_id:
task_id:
failure_type:
observed_problem:
root_cause:
preventive_rule:
retry_history:
timestamp:
```
