# 강의교안 탐색적 리서치 (Phase 2) 세부 워크플로우

> **핵심 차이**: 구성안 Phase 2는 "무엇을 가르칠까?(What)" → 교안 Phase 2는 "어떻게 가르칠까?(How)"

## 전체 흐름

```
Step 0: 스키마 참조 + 입력 로드 + 리서치 계획 수립
  │     input-schema-script.json (스키마 사전 이해)
  │     + input_data.json (script_config 포함) + 구성안 3파일 → research_plan.md
  │
  ├── Step 1: 로컬 참고자료 분석 → local_findings.md
  │   (조건: script_config.reference_sources.local_folders 비어있으면 건너뜀)
  │
  ├── Step 2: NotebookLM 소스 쿼리 → nblm_findings.md
  │   (조건: script_config.reference_sources.notebooklm_urls 비어있으면 건너뜀)
  │
  ├── Step 3: 인터넷 리서치 → web_findings.md
  │   (교수법 사례 + 유사 교안 벤치마킹 + 실생활 사례 + 학습활동 설계)
  │
  └── Step 4: 4자료원 통합 → research_exploration.md
      (주제 축 추출 → 축별 배정 → 교차검증 → 고착필터 → 구조화 작성)
```

## 산출물 목록

```
{output_dir}/    (= 02_script/)
├── research_plan.md          # Step 0: 리서치 계획
├── local_findings.md         # Step 1: 로컬 참고자료 분석 결과
├── nblm_findings.md          # Step 2: NotebookLM 쿼리 결과
├── web_findings.md           # Step 3: 인터넷 리서치 결과
└── research_exploration.md   # Step 4: 4자료원 통합 최종 산출물 ★
```

---

## Step 0: 스키마 참조 + 입력 로드 + 리서치 계획 수립

| 항목 | 내용 |
|------|------|
| 스키마 참조 | `.claude/templates/input-schema-script.json` — 필드 의미·유효값·관계 이해용 |
| 입력 | `{output_dir}/input_data.json`, `{source_outline.outline_path}`, `{source_outline.architecture_path}` |
| 도구 | Read, Write |
| 산출물 | `{output_dir}/research_plan.md` |

**동작**:

1. `.claude/templates/input-schema-script.json` 읽기 — **스키마 사전 이해**:
   - `script_config` 각 필드의 의미(description)와 유효 enum 값 파악
   - `teaching_model` enum (`direct_instruction`/`pbl`/`flipped`/`mixed`)과 교수설계 모델 매핑 이해
   - `activity_strategies` enum과 활동 유형 이해
   - `formative_assessment` 구조 (primary_type, assessment_plan, slo_coverage) 이해
   - `instructional_model_map` (primary_model, grr_focus, bloom_question_pattern) 관계 이해
   - `bloom_question_map.per_session` 구조 (차시별 수업 단계별 발문 수준) 이해
2. `input_data.json` 읽기 — 스키마 기반으로 핵심 필드 추출:
   - `topic`(Q1), `target_learner`(Q2), `learning_goals`(Q3), `keywords`(Q6)
   - `lab_environment`(Q14)
   - `script_config.teaching_model`(S1a), `script_config.activity_strategies`(S1b)
   - `script_config.formative_assessment`(S3), `script_config.bloom_question_map`(S6)
   - `script_config.instructional_model_map` (교수설계 모델 조합)
   - `script_config.reference_sources`(S5)
3. `lecture_outline.md` 읽기 — 차시 구조, SLO 목록, 하위 주제 추출
4. `architecture.md` 읽기 — Gagne 9사태 적용 계획, GRR 패턴, 형성평가 배치 확인
5. 리서치 질문 자동 도출 (**교안 특화 5~7개**, 스키마의 필드 의미와 enum 기반):
   - "이 주제를 {teaching_model} 모델로 가르친 교안/수업 설계 사례는?"
     (스키마 `instructional_model_map.primary_model`로 구체적 모델명 반영: Hunter_6step/PBL_6step/Before_During_After)
   - "이 주제에서 효과적인 {activity_strategies} 활동 패턴은?"
     (스키마 enum: individual_practice/group_activity/discussion/project)
   - "학습자가 자주 오해하는 개념과 이를 해소하는 설명 전략은?"
   - "도입부에서 학습자 주의를 끄는 훅(Hook) / 실생활 사례는?"
   - "Bloom's {bloom_level} 수준에 적합한 발문 패턴은?"
     (스키마 `bloom_question_map.per_session`의 intro/main/wrap_question_level 반영)
   - "{formative_assessment.primary_type}에 효과적인 구체적 평가 도구는?"
     (스키마 enum: sectional_check/exit_ticket/practice_integrated/mixed)
   - (교수 모델별 조건부) "{instructional_model_map.grr_focus}의 구체적 전환 사례는?"
     (스키마 enum: i_do_we_do_you_do/you_do_together/we_do_you_do_together)
6. `research_plan.md` 작성:
   - 리서치 질문 목록 (스키마 enum 값 반영)
   - 서브토픽 분류 (3~5개, 아래 §Step 3 참조)
   - 자료원별 검색 예산 (웹 검색 최대 15회, NBLM 쿼리 최대 5회)
   - 스키마 참조 요약 (어떤 필드가 리서치 방향에 영향을 주었는지 기록)

---

## Step 1: 로컬 참고자료 분석

구성안 Phase 2 Step 1과 **동일한 구조** 재사용. 차이점:

| 항목 | 구성안 | 교안 |
|------|--------|------|
| 입력 경로 | `input_data.json → reference_sources.local_folders` | `input_data.json → script_config.reference_sources.local_folders` |
| 분석 관점 | 주제 본질, 학습자 배경, 트렌드 | **교수법 시사점, 활동 설계 아이디어, 설명 전략, 실습 예제** |
| 파일별 요약 초점 | 핵심 내용 200~400자 | 핵심 내용 + "**교안 활용 포인트**" (어떤 차시/단계에서 활용 가능한지) |

| 항목 | 내용 |
|------|------|
| 입력 | `script_config.reference_sources.local_folders` |
| 조건 | 배열이 비어있으면 건너뜀 → `local_findings.md`에 "로컬 참고자료 없음" 기록 |
| 도구 | Glob, Read, Bash(pdf/docx 텍스트 추출), Write |
| 산출물 | `{output_dir}/local_findings.md` |

**파일 읽기**: `shared/file-reading-strategy.md`를 Read하여 확장자별 읽기 전략을 따른다.

**동작**: 구성안 Phase 2 Step 1과 동일. 확장자별 읽기 전략 재사용.

파일별 요약 시 아래 형식 준수:
```
### {파일명}
- **핵심 내용**: (200~400자)
- **교안 활용 포인트**: (어떤 차시/단계에서, 어떤 교수법 맥락으로 활용 가능한지)
```

---

## Step 2: NotebookLM 소스 쿼리

구성안 Phase 2 Step 2와 **동일한 구조** 재사용. 차이점:

| 항목 | 구성안 | 교안 |
|------|--------|------|
| 입력 경로 | `reference_sources.notebooklm_urls` | `script_config.reference_sources.notebooklm_urls` |
| 질문 생성 전략 | 주제 본질·학습자·트렌드 질문 | **교수법·활동·사례 질문** |

| 항목 | 내용 |
|------|------|
| 입력 | `script_config.reference_sources.notebooklm_urls` |
| 조건 | 배열이 비어있으면 건너뜀 → `nblm_findings.md`에 "NotebookLM 소스 없음" 기록 |
| 도구 | Bash(`/nblm`), Write |
| 산출물 | `{output_dir}/nblm_findings.md` |

**NBLM 호출**: `shared/nblm-interface.md`를 Read하여 CLI 명령과 후속 질문 프로토콜을 따른다.

### 교안용 NBLM 질문 생성 전략

`research_plan.md`의 리서치 질문을 NBLM용으로 변환:
1. "이 자료에서 {topic}을 가르치는 효과적인 방법이나 교수 전략은?"
2. "이 자료에서 실습이나 활동으로 활용할 수 있는 구체적 예시는?"
3. "이 자료에서 학습자가 자주 어려워하는 부분과 해결 방법은?"
4. "이 자료에서 {teaching_model}에 적합한 수업 운영 패턴은?"
5. (필요시) "이 자료에서 평가나 학습 확인에 활용할 수 있는 방법은?"

---

## Step 3: 인터넷 리서치 (web-research 패턴)

구성안 Phase 2 Step 3과 **동일한 구조** (3a 계획 → 3b 검색 → 3c 심화).

| 항목 | 내용 |
|------|------|
| 입력 | `research_plan.md`의 리서치 질문 + 서브토픽 |
| 도구 | WebSearch, WebFetch, Write |
| 산출물 | `{output_dir}/web_findings.md` |
| 예산 | 웹 검색 최대 15회 |

### 서브토픽 분류 (교안 특화)

| 서브토픽 | 검색 목적 | 검색 예산 |
|---------|----------|----------|
| **교수 모델 사례** | teaching_model에 맞는 수업 설계 패턴·교안 사례 | 3~4회 |
| **학습활동 설계** | activity_strategies별 구체적 활동 패턴·도구 | 3~4회 |
| **실생활 사례·훅** | 도입부 훅, 동기부여 사례, 실무 활용 사례 | 2~3회 |
| **발문·평가 도구** | Bloom's 수준별 발문, 형성평가 도구 사례 | 2~3회 |
| **학습자 오개념·장벽** | 흔한 오해, 학습 장벽, 설명 전략 | 2~3회 |

### 교수 모델별 검색어 분기

```
teaching_model = direct_instruction:
  "{topic} lesson plan direct instruction" / "{topic} 수업지도안 직접교수법"
  "Hunter lesson plan template {topic}" / "I Do We Do You Do {topic}"

teaching_model = pbl:
  "{topic} PBL lesson plan" / "{topic} 프로젝트 기반 학습 교안"
  "problem-based learning {topic} scenario" / "{topic} PBL 문제 시나리오"

teaching_model = flipped:
  "{topic} flipped classroom lesson plan" / "{topic} 플립러닝 수업설계"
  "flipped learning {topic} in-class activity" / "사전학습 {topic}"

공통:
  "{topic} teaching strategies {target_learner}" / "{topic} 교수법 {target_learner}"
  "{topic} common misconceptions" / "{topic} 초보자 실수 오해"
  "{topic} formative assessment examples" / "{topic} 형성평가 도구"
  "Bloom's taxonomy questions {topic}" / "{topic} 발문 예시"
  "{topic} real world examples teaching" / "{topic} 실생활 사례 교육"
```

### 고착 효과 방지 필터 (교안 버전)

구성안과 동일한 원칙이지만 **필터 대상이 다름**:

```
허용 (O):
  "이 강의는 실습 중심 접근법을 사용한다" — 교수법 방향성
  "PBL에서는 문제 시나리오를 먼저 제시한다" — 교수 모델 패턴
  "Think-Pair-Share를 5분간 진행한다" — 활동 설계 패턴
  "이 개념은 학습자가 자주 혼동한다" — 학습자 어려움
  "실습 체크리스트로 이해도를 확인한다" — 평가 도구 패턴

금지 (X):
  "[강사] 여러분, 오늘은 ..." — 구체적 강사 대본/발화문
  "슬라이드 1: 제목, 슬라이드 2: 개요..." — 슬라이드 구성 전사
  "차시 1 교안: 도입(5분) '안녕하세요...' " — 특정 교안의 시간·대본 직접 복제

변환 규칙:
  "도입 5분: '안녕하세요, 오늘은 X를 배웁니다'"
    → "도입부에서 학습 목표를 일상 언어로 제시하는 접근법"
  "전개 30분: 예제 코드를 한 줄씩 설명"
    → "코드 예제를 점진적으로 제시하는 scaffolding 접근법"
```

---

## Step 4: 4자료원 통합 → research_exploration.md

| 항목 | 내용 |
|------|------|
| 입력 | `research_plan.md`, `local_findings.md`, `nblm_findings.md`, `web_findings.md` |
| 도구 | Read, Write |
| 산출물 | `{output_dir}/research_exploration.md` ★ |

### 4-1. 자료원별 역할과 신뢰도

| 자료원 | 역할 | 신뢰도 | 활용 단계 |
|--------|------|--------|----------|
| **input-schema-script.json** | 구조 참조 — 필드 의미·유효 enum·필드 간 관계 정의. 다른 자료원 해석과 통합 검증의 기준 | ★★★ 절대 기준 | Step 0(사전 이해) + Step 4(축 추출·배정·교차검증·문서 작성) |
| **input_data.json** | 설계 기준선 — 모든 판단의 절대 기준. 스키마에 정의된 구조에 따른 실제 값 | ★★★ 절대 기준 | Step 0(필드 추출) + Step 4(축 추출) |
| **구성안 산출물** | 차시 구조·SLO·학습자 프로필 — 변경 금지 기준 | ★★★ 절대 기준 | Step 0(구조 파악) + Step 4(교차검증) |
| **로컬 참고자료** | 사용자 선별 핵심 자료 | ★★★ 높음 | Step 1(분석) + Step 4(통합) |
| **NotebookLM** | 사용자 선별 소스 기반 검증된 답변 | ★★★ 높음 | Step 2(쿼리) + Step 4(통합) |
| **인터넷 리서치** | 최신 교수법 사례, 외부 벤치마킹 | ★☆☆~★★☆ 가변 | Step 3(검색) + Step 4(통합) |

> 구성안과의 차이: `input-schema-script.json`(구조 참조)과 `구성안 산출물`이 자료원으로 추가됨

**스키마의 통합 알고리즘 내 역할**:

| 통합 단계 | input-schema-script.json 활용 |
|----------|------------------------------|
| 단계 1 (축 추출) | `script_config` 필드 구조와 description으로 5개 축의 범위와 경계 정의 |
| 단계 2 (축별 배정) | enum 값으로 인사이트→필드 매핑 검증 (예: 수집된 활동이 `activity_strategies` enum에 해당하는지) |
| 단계 3 (교차검증) | `instructional_model_map` 관계로 교수법 인사이트 간 정합성 검증 (예: teaching_model과 grr_focus 일관성) |
| 단계 5 (문서 작성) | 필드별 description으로 각 섹션의 내용 범위와 깊이 결정 |

### 4-2. 통합 알고리즘 (5단계) — 주제 축 재설계

**단계 1 — 주제 축(Theme Axis) 추출 (교안 특화 5개 축)**

| 축 | 질문 | 매핑 섹션 | 구성안 축과의 차이 |
|----|------|----------|-----------------|
| **A: 교수법 패턴** | "이 주제를 어떤 방식으로 가르치는 것이 효과적인가?" | §1 교수 모델별 수업 설계 사례 | 구성안 D축(교육 현황) 대체 — 교안은 "어떻게" 초점 |
| **B: 학습활동·참여** | "어떤 활동이 학습 참여와 이해를 높이는가?" | §2 학습활동·참여 전략 사례 | 신규 축 — 구성안에 없음 |
| **C: 설명·사례·비유** | "학습자에게 어떤 설명/사례/비유가 효과적인가?" | §3 실생활 사례·설명 전략 | 구성안 A축(주제 본질) + E축(실무) 재조합 |
| **D: 학습자 장벽·오개념** | "학습자가 자주 겪는 어려움과 오해는 무엇이며 어떻게 해소하는가?" | §4 학습자 오개념·장벽 해소 전략 | 구성안 B축(학습자) 심화 — 해소 전략 포함 |
| **E: 평가·발문·피드백** | "학습 확인을 위한 효과적인 발문·평가·피드백 방법은?" | §5 발문·형성평가·피드백 패턴 | 신규 축 — 구성안에 없음 |

**단계 2 — 자료원별 인사이트를 축에 배정**

구성안과 동일한 알고리즘 재사용:
- 각 인사이트를 가장 관련 높은 축에 배정
- 복수 축에 걸치는 경우 주 축 + 부 축 태깅
- 미배정 인사이트는 가장 가까운 축에 강제 배정 또는 별도 기록

**단계 3 — 교차 검증 및 충돌 해결**

`shared/triangulate-rules.md`를 Read하여 교차검증 규칙을 따른다.

우선순위: 스키마 정의 = input_data = 구성안 > 로컬 = NBLM > 웹

- 스키마 enum에 정의되지 않은 값이 인터넷 리서치에서 발견되면 → 가장 가까운 enum 값으로 매핑하거나 `[스키마 외]` 태그
- `instructional_model_map` 관계로 교수법 인사이트 간 정합성 검증

**단계 4 — 고착 효과 필터링**

위 "고착 효과 방지 필터 (교안 버전)" 적용

**단계 5 — 구조화된 문서 작성**

아래 산출물 구조에 따라 `research_exploration.md` 작성

### research_exploration.md 산출물 구조 (교안 전용)

```markdown
# 강의교안 탐색적 리서치 결과

## 메타데이터
- 강의 주제: {topic}
- 리서치 일자: {date}
- 교수 모델: {teaching_model}
- 활동 전략: {activity_strategies}
- 자료원 현황: 로컬 {N}건, NBLM {N}건, 웹 {N}건
- 리서치 모드: 탐색적 (orientation) — 고착 효과 방지 필터 적용
- 리서치 초점: 교수법 실행 (How to teach)

---

## 1. 교수 모델별 수업 설계 사례
(축 A. {teaching_model}에 맞는 수업 운영 패턴, 도입-전개-정리 사례)

### 1-1. {teaching_model} 모델의 일반적 수업 흐름
(예: Hunter 6단계 적용 사례, PBL 문제 시나리오 패턴 등)

### 1-2. 유사 주제 교안 벤치마킹
(유사 주제를 가르치는 강의의 교수법 접근 — ★ 구체적 대본/시간표 노출 금지)

### 1-3. GRR(점진적 책임 이양) 적용 패턴
(I Do→We Do→You Do 전환 사례 — teaching_model별 중심 단계 상이)

- 시사점: ...

---

## 2. 학습활동·참여 전략 사례
(축 B. activity_strategies별 구체적 활동 설계 패턴)

### 2-1. {activity_strategy_1} 활동 사례
(예: 개인 실습 — 단계별 안내 실습 → 독립 실습 전환 패턴)

### 2-2. {activity_strategy_2} 활동 사례
(예: 그룹 활동 — Think-Pair-Share, Jigsaw, 페어 프로그래밍 등)

### 2-3. 활동 시퀀스 설계 패턴
(심리적 안전감 구축 → 참여 활동 → 성찰 활동의 흐름)

- 시사점: ...

---

## 3. 실생활 사례·설명 전략
(축 C. 학습자 동기 부여 사례, 도입부 훅, 비유/메타포, 실무 활용 예시)

### 3-1. 도입부 훅(Hook) / 주의 획득 사례
(Gagne 사태 1: 학습자 주의를 끄는 스토리, 질문, 데이터, 시연)

### 3-2. 핵심 개념별 설명 전략·비유
(예시-비예시 쌍, 메타포, 시각화 방법)

### 3-3. 실무 활용 사례
(학습자가 "이 기술을 왜 배우는가?"에 답하는 실제 사용 사례)

- 시사점: ...

---

## 4. 학습자 오개념·장벽 해소 전략
(축 D. 흔한 오해, 학습 장벽, 해소 전략)

### 4-1. 도메인별 주요 오개념 (Misconceptions)
(학습자가 자주 오해하는 개념 3~7개, 출처 포함)

### 4-2. 학습 장벽 및 어려운 지점 (Bottlenecks)
(심리적 장벽, 인지적 장벽, 기술적 장벽)

### 4-3. 해소 전략 (Resolution Strategies)
(오개념별 명시적 개입 설계: 어떤 시점에서 어떤 방식으로 교정하는가)

- 시사점: ...

---

## 5. 발문·형성평가·피드백 패턴
(축 E. Bloom's 수준별 발문 사례, 형성평가 도구, 피드백 방법)

### 5-1. Bloom's 수준별 발문 사례
(기억 L1 ~ 창조 L6 각 수준별 도메인 맥락화 발문 2~3개)

### 5-2. 형성평가 도구 사례
({formative_assessment.primary_type}에 적합한 구체적 도구/방법)

### 5-3. 피드백 패턴
(즉각 피드백 vs 지연 피드백, 피드백 문장 패턴, 동료 평가 가이드)

### 5-4. Gagne 9사태 실행 가이드
(9사태별 교안에서의 구체적 구현 패턴 — 체크리스트용)

| 사태 | 이름 | 교안 구현 패턴 사례 |
|------|------|------------------|
| 1 | 주의 획득 | {도입부 훅 사례 — §3-1 연동} |
| 2 | 목표 고지 | {학습 목표 일상 언어 제시 패턴} |
| 3 | 선수 학습 자극 | {선수 지식 확인 질문 패턴} |
| 4 | 자극 자료 제시 | {멀티미디어 학습 원리 적용 방식} |
| 5 | 학습 안내 | {비계(scaffold) 유형별 적용 시점} |
| 6 | 수행 유도 | {연습 문제 유형, 수행 과제 패턴} |
| 7 | 피드백 제공 | {피드백 문장 패턴 — §5-3 연동} |
| 8 | 수행 평가 | {형성평가 도구 — §5-2 연동} |
| 9 | 파지·전이 촉진 | {실무 적용 시나리오 — §3-3 연동} |

- 시사점: ...

---

## 6. 참고자료 분석 요약

### 6-1. 로컬 자료
(파일별: 파일명, 핵심 내용 3줄, **교안 활용 포인트**)

### 6-2. NotebookLM 소스
(쿼리별: 질문, 핵심 응답 3줄, 인용된 소스)

---

## 7. 리서치 인사이트 (Phase 3 브레인스토밍용)
(5~10개 방향성 인사이트)

각 인사이트:
- "~라는 교수법/접근/활동 패턴이 있다" 형식
- 관련 SLO 태깅
- 관련 activity_strategy 태깅
- 관련 Bloom's 수준 태깅
- 구체적 대본/교안 내용 제외

---

## 출처 목록
| # | 출처 | 유형 | 접근일자 | 신뢰도 |
|---|------|------|---------|--------|
| [1] | {URL/파일경로} | 로컬/NBLM/웹 | {날짜} | [검증됨/미검증] |
```
