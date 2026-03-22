# LLM 무시/강제 중단 리스크 평가와 개선

## 1) 필요성 평가
### 현재 상태
- `MockRuntime` 데모 자체는 외부 LLM 호출이 없어 즉시 위험은 낮다.
- 하지만 실제 모델 연결 시, 출력 포맷 위반/체인브레이크 문자열/역할 경계 위반이 상태 머신을 깨뜨릴 수 있다.

### 결론
- **개선이 필요**하며, 특히 "역할별 I/O 계약", "복구 루프", "실행 컨텍스트 주입"이 필수다.

## 2) 반영한 개선
1. **역할별 입출력 계약 강제**
   - Starter 8 역할의 required fields를 코드에서 검증.
   - critic/qa의 verdict 허용값을 화이트리스트로 제한.
2. **프롬프트 파일 연결**
   - `PromptRegistry`로 `agents/prompts/{role}.md`를 로드해 호출.
3. **실패 복구형 supervisor loop**
   - REVIEW_FAILED: 재계획 루프(최대 2회) 후 3회 실패 시 human escalation 반환.
   - QA_FAILED: 재진입 루프(최대 2회) 후 에스컬레이션 반환.
   - step/time budget 가드를 도입.
4. **메모리 retrieval layer**
   - 다음 agent 호출 전에 policy, active task, 최근 decisions/failures, knowledge summaries를 자동 주입.
5. **체인브레이크 탐지 + 재시도**
   - `ignore previous`, `shutdown`, `stop execution` 등 위험 패턴 감지 시 재시도 후 중단.

## 3) 운영 권장
- 실제 OpenClaw 연동 시 role별 schema validation을 서버측에서도 이중 적용.
- 고위험 작업(비용 집행/배포/삭제)은 human approval gate 필수.
- 반복 failure pattern은 `policy/`에 예방 규칙으로 승격.


## 4) 판정 원칙
- 모델 verdict는 참고값이고, 최종 게이트 판정은 evaluator 점수 임계값으로 하네스가 결정한다.
