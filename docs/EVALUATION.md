# EVALUATION

## 평가 축
### 기본
- goal_alignment
- factuality
- completeness
- logic
- reproducibility
- quality

### 확장
- originality
- usefulness
- clarity
- market_value
- differentiation

## 점수 예시
```yaml
scores:
  goal_alignment: 0-5
  factuality: 0-5
  completeness: 0-5
  logic: 0-5
  reproducibility: 0-5
  quality: 0-5
  originality: 0-5
  usefulness: 0-5
  clarity: 0-5
  market_value: 0-5
  differentiation: 0-5

thresholds:
  pass: 40+
  repair: 26-39
  fail: 0-25
```

## 판정 정책
- pass: 다음 단계 진행
- repair: Repair Loop 진입
- fail: Replanning 또는 Rollback

## 리포트 최소 항목(EvalReport)
- artifact_id
- verdict
- axis별 점수와 근거
- risk_level
- repair_instructions(필요 시)
- 최종 추천 행동(next action)
