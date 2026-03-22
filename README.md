# autonomous-openclaw (Harness Scaffold)

이 저장소는 문서로 고정한 운영 설계를 실제 **에이전트 하네스 구조**로 옮긴 최소 실행 골격입니다.

## 포함 내용
- 상태 머신 + 전이 가드
- GoalSpec/TaskSpec/EvalSpec/DecisionSpec/FailureSpec 데이터 모델
- 메모리 저장소(memory/) 초기화 및 이벤트/결과 저장
- OpenClaw 실행 런타임 어댑터 인터페이스(현재는 MockRuntime)
- Stage-1 데모 루프 (Goal Ingestion → Plan → Build → Critic → Repair(optional) → Finalize)

## 빠른 실행
```bash
python -m orchestrator.main --demo
```

실행 후 아래가 생성됩니다.
- `runtime/state.db`
- `memory/tasks/*`, `memory/evaluations/*`, `memory/failures/*`, `memory/decisions/*`
- `artifacts/drafts/`, `artifacts/final/`

## 다음 단계
1. `runtime/openclaw_runtime.py`의 `MockRuntime`을 실제 OpenClaw 호출로 교체
2. Critic/QA 프롬프트를 `agents/prompts/*.md`와 연결
3. Queue/Lock(예: Redis), 멀티 워커, 병렬 디스패처 추가
