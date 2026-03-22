# WORKFLOW

## 상태 머신
GOAL_INGESTED
→ MISSION_LOCKED
→ PLAN_CREATED
→ TASKS_CREATED
→ TASKS_ASSIGNED
→ IN_PROGRESS
→ SUBMITTED_FOR_REVIEW
→ REVIEW_FAILED / REVIEW_REPAIR / REVIEW_PASSED
→ REPAIRING
→ INTEGRATING
→ QA_REVIEW
→ QA_FAILED / QA_PASSED
→ FINAL_PACKAGING
→ DELIVERED
→ RETROSPECTIVE_STORED
→ KNOWLEDGE_UPDATED

## 페이즈
1. Goal Ingestion: 입력을 GoalSpec으로 구조화
2. Mission Lock: 목표/제약/우선순위 고정
3. Planning: Task tree + dependency map 생성
4. Parallel Exploration: 독립 리서치/설계 병렬 탐색
5. Build: 산출물 초안 생성
6. Critical Review: Critic 판정(pass/repair/fail)
7. Repair Loop: 수정 지시 반영 및 재검수
8. Integration: 산출물 병합/충돌 해소
9. QA: 실행성/재현성/누락 검사
10. Final Packaging: 최종 산출물 패키징
11. Retrospective: 성공/실패 교훈 저장
12. Continuous Learning: 신규 지식 반영

## 운영 규칙
- 탐색은 병렬, 결정은 순차, 통합은 중앙
- repair 최대 2회, 이후 replanning
- 3회 fail 시 rollback 또는 human escalation
