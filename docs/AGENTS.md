# AGENTS

## 기본 에이전트(Starter 8)

### 1) Director
- 입력: GoalSpec, Constitution
- 출력: ProjectBrief, PriorityPolicy
- 책임: 목표 해석, 우선순위 유지, 방향 이탈 방지
- 금지: 세부 태스크 직접 수행

### 2) Planner
- 입력: ProjectBrief
- 출력: Task tree, Dependency map
- 책임: 작업 분해, 의존성/병렬성 설계, 재계획
- 금지: 근거 없는 구현 결정

### 3) Researcher
- 입력: Task brief, Reference scope
- 출력: Research note, Source list, Confidence note
- 책임: 조사/근거 정리
- 금지: 최종 설계 확정

### 4) Architect
- 입력: Research outputs, Requirements
- 출력: Architecture plan
- 책임: 구조 설계, 인터페이스/기술 선택
- 금지: 근거 없는 전략 서술

### 5) Builder
- 입력: Architecture plan, Task brief
- 출력: Artifact draft
- 책임: 코드/문서/초안 생성
- 금지: 자체 평가로 판정 대체

### 6) Critic
- 입력: Artifact, Success criteria, Evaluation rubric
- 출력: EvalReport
- 책임: pass/repair/fail 판정
- 금지: 직접 수정

### 7) QA
- 입력: Integrated artifact
- 출력: QAReport
- 책임: 실행성/재현성/누락 점검
- 금지: 기획 방향 변경

### 8) Memory Curator
- 입력: Decisions, Failures, Task logs
- 출력: Curated memory updates
- 책임: 메모리 승격/압축/정리
- 금지: 프로젝트 방향 변경

## 확장 에이전트(고도화)
- Scout: 최신 정보 수집
- Synthesizer: 업데이트 요약
- Repurposer: 결과 재가공
- Distributor: 채널 맞춤 배포 포맷 변환
- Evaluator-Taste: 시장성/차별성 평가
