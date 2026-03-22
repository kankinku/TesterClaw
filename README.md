# autonomous-openclaw (Harness Scaffold)

이 저장소는 문서로 고정한 운영 설계를 실제 **에이전트 하네스 구조**로 옮긴 최소 실행 골격입니다.

## 포함 내용
- 상태 머신 + 전이 가드
- GoalSpec/TaskSpec/EvalSpec/DecisionSpec/FailureSpec 데이터 모델
- 메모리 저장소(memory/) + 실행 컨텍스트 retrieval layer
- OpenClaw 실행 런타임 어댑터 인터페이스(현재는 MockRuntime)
- 역할별 프롬프트 파일 로딩 (`agents/prompts/*.md`)
- 역할별 출력 계약 검증 + 체인 브레이킹 패턴 필터 + 재시도 가드
- supervisor loop 기반 실패 복구 (replan / qa re-entry / escalation)
- evaluator gate 점수 판정(모델 verdict 참고 + 하네스 최종 판정)
- observability: SQLite `agent_runs` 지표 기록

## 빠른 실행
```bash
python -m orchestrator.main --demo
```

실행 후 아래가 생성됩니다.
- `runtime/state.db`
- `memory/tasks/*`, `memory/evaluations/*`, `memory/failures/*`, `memory/decisions/*`
- `artifacts/drafts/`, `artifacts/final/`

## 보안/안정성 문서
- `docs/LLM_GUARDRAILS.md`: LLM 통합 시 무시/강제중단 리스크와 하네스 개선 사항

## 다음 단계
1. `runtime/openclaw_runtime.py`의 `MockRuntime`을 실제 OpenClaw 호출로 교체
2. planner/builder/critic/qa 외 역할(researcher/architect/memory_curator) supervisor 경로 확장
3. Queue/Lock(예: Redis), 멀티 워커, 병렬 디스패처 추가


## 테스트
```bash
python -m unittest tests.contracts.test_contracts tests.workflows.test_supervisor
```


## 브랜치/머지 체크
메인 브랜치로 머지가 안 될 때는 아래를 먼저 확인하세요.

```bash
git branch -vv
```

- `main` 브랜치가 없으면 생성:
```bash
git branch main 8c7f821
```
- 최신 작업 브랜치(`work`)를 메인으로 fast-forward:
```bash
git checkout main
git merge --ff-only work
```
- 다시 작업 브랜치로 복귀:
```bash
git checkout work
```
