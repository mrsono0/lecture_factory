# 강의교안 심화 리서치 (Phase 4) 세부 워크플로우

## 개요

브레인스토밍 결과(brainstorm_result.md §7)의 구체적 요청사항을 **deep-research 스킬의 8단계 파이프라인**에 따라 검증·보충한다.

구성안 Phase 4와의 핵심 차이:

| 차원 | 구성안 Phase 4 | 교안 Phase 4 |
|-----|---------------|-------------|
| 입력 컬럼 | `관련 하위 주제` | `관련 차시/SLO` |
| 검증 초점 | 콘텐츠 사실 확인(What) | 교수법 효과성 검증(How to teach) |
| 요청 유형 | 사례 검증, 참고 문헌, 사실 확인 | 사례 검증, 활동 보충, 사실 확인 |
| 삼각검증 기준 | 콘텐츠 정확성 (3중 소스 일치) | 효과 크기 + 맥락 전이 + SLO 측정 타당성 |
| 산출물 소비자 | Phase 5 (architecture-agent) | Phase 5 (architecture-agent) + Phase 6 (writer-agent) |

Phase 2(탐색적 리서치)와의 핵심 차이:

| 차원 | Phase 2 (탐색적) | Phase 4 (심화) |
|-----|-----------------|---------------|
| 입력 | input_data.json (Q1~Q11) | brainstorm_result.md §7 요청 사항 |
| 범위 | 넓고 얕게 (문제 공간 이해) | 좁고 깊게 (아이디어 검증) |
| 고착 필터 | 강제 적용 (대본/교안 내용 제외) | 미적용 (구체적 해결책 수준까지 진입 가능) |
| 리서치 방법론 | web-research 패턴 (4자료원 통합) | deep-research 스킬 8단계 파이프라인 |
| 산출물 | 7섹션 통합 문서 (방향성 인사이트) | 요청별 섹션화 문서 (검증 결과 + 보충 자료) |

## 전체 흐름

```
Step 0: 입력 변환 + 심화 리서치 계획 수립
  │     brainstorm_result.md §7 + input_data.json + 구성안(outline/architecture) → deep_research_plan.md
  │     (§7 요청을 deep-research 입력 형식으로 변환, §1·§2·§5 컨텍스트 로드)
  │
  ├── Step 1: deep-research 스킬 지침에 따른 리서치 수행
  │     (.claude/skills/deep-research/SKILL.md 읽기 → 8단계 파이프라인 실행)
  │     ├── Scope: 요청별 리서치 범위 정의 (교수법 효과성 기준)
  │     ├── Plan: 검색 전략 수립 (사례검증/활동보충/사실확인 유형별 차별화)
  │     ├── Retrieve: 로컬 분석 → NBLM 쿼리 → 웹 검색 (3자료원 필수)
  │     ├── Triangulate: 3중 소스 교차검증 + 교수법 효과성 3중 검증
  │     ├── Synthesize: 통합 인사이트 생성
  │     ├── Critique: 교수 모델 정합성 검증, 반대 증거 탐색
  │     └── Refine: 공백 해소, 인용 정확성 검증
  │     → verification_results.md + supplement_results.md
  │
  └── Step 2: 출력 정규화 + Phase 5·6 전달용 통합
        (deep-research 결과 → research_deep.md 프로젝트 형식)
```

## 산출물 목록

```
{output_dir}/
├── deep_research_plan.md      # Step 0: 심화 리서치 계획 (입력 변환)
├── verification_results.md    # Step 1: 검증 유형 수집 결과
├── supplement_results.md      # Step 1: 보충 유형 수집 결과
└── research_deep.md           # Step 2: 최종 통합 산출물 ★
```

---

## Step 0: 입력 변환 + 심화 리서치 계획 수립

| 항목 | 내용 |
|------|------|
| 입력 | `{output_dir}/brainstorm_result.md` §1·§2·§5·§7, `{output_dir}/input_data.json`, `{source_outline.outline_path}`, `{source_outline.architecture_path}` |
| 도구 | Read, Write |
| 산출물 | `{output_dir}/deep_research_plan.md` |

**동작**:

1. `brainstorm_result.md` §7 파싱 — 요청 테이블 추출:
   - `#` (요청 번호), `유형` (사례 검증/활동 보충/사실 확인), `요청 내용`, `관련 차시/SLO`, `우선순위`
   - **주의**: 구성안 §7은 `관련 하위 주제` 컬럼이나, 교안 §7은 `관련 차시/SLO` 컬럼 사용
2. `brainstorm_result.md` §1·§2·§5 컨텍스트 로드:
   - §1(발문 설계): Bloom's 수준별 발문 → 발문 검증의 기준선
   - §2(학습활동): GRR × 차시별 활동 아이디어 → 활동 보충 검색의 컨텍스트
   - §5(Gagne 구현): 9사태 구현 초안 → 교수법 검증의 참조
3. `input_data.json` 핵심 필드 재확인:
   - `topic`, `target_learner`, `learning_goals`, `keywords`
   - `lab_environment` (Q14)
   - `script_config.teaching_model` — 교수 모델 (direct_instruction/pbl/flipped/mixed)
   - `script_config.instructional_model_map` — 교수설계 모델 (primary_model, grr_focus, bloom_question_pattern)
   - `script_config.formative_assessment` — 형성평가 계획 (primary_type, assessment_plan)
   - `script_config.reference_sources` — 3자료원 경로 (local_folders, notebooklm_urls, web_research)
4. 구성안 참조 (변경 불가 기준):
   - `source_outline.outline_path` → lecture_outline.md 로드 (차시별 SLO 확인)
   - `source_outline.architecture_path` → architecture.md 로드 (시간 배분, Bloom's 수준 확인)
5. 각 요청을 deep-research 입력 형식으로 변환:
   - 요청 내용 → 명확한 리서치 질문으로 재구성
   - 유형(사례 검증/활동 보충/사실 확인) → 검색 전략 힌트 (아래 표 참조)
   - `관련 차시/SLO` → 검증 컨텍스트 (architecture.md의 해당 차시 정보 참조)
   - 우선순위 → 처리 순서 + 검색 예산 배분
6. 3자료원 분석 계획 수립 (로컬 · NBLM · 웹 모두 필수):
   - 로컬 참고자료: 각 요청에 대해 `script_config.reference_sources.local_folders`에서 탐색할 심화 질문 설계
   - NotebookLM: 각 요청에 대해 `script_config.reference_sources.notebooklm_urls`에서 던질 심화 질문 설계
   - 웹: 유형별 검색 전략에 따른 검색어 설계
7. deep-research 실행 모드 결정: **Standard** (기본) 또는 **Deep** (높음 우선순위 다수 시)
8. `deep_research_plan.md` 작성

### 유형별 검색 전략 (교안 특화)

| 유형 | 목적 | 우선 소스 | 검증 기준 |
|------|------|----------|----------|
| **사례 검증** | 교수법/활동 전략의 근거 확인 | 메타분석 → 대학 CTL → 교사 커뮤니티 | 효과 크기 + 맥락 전이 필수 (Triangulate) |
| **활동 보충** | 루브릭/발문/활동 템플릿 수집 | 대학 CTL → 교육공학 저널 → 교사 커뮤니티 | SLO 적합성 + 현실 적용 가능성 |
| **사실 확인** | 교수설계 이론/원칙 검증 | 공식 교수설계 문헌 → 논문 → 전문가 블로그 | 3중 소스 일치 필수 (Triangulate) |

### 교수 모델별 검색어 예시

```
사례 검증 예시:
  "{teaching_model} effectiveness meta-analysis"
  "Gagne instructional events evidence classroom"
  "gradual release responsibility {target_learner} evidence"
  "{교수 모델} 효과성 연구 메타분석"

활동 보충 예시:
  "{topic} rubric template {Bloom's level}"
  "Bloom's taxonomy question bank {topic}"
  "{topic} formative assessment {SLO keyword}"
  "{주제} 활동지 템플릿 {학습자 수준}"

사실 확인 예시:
  "gradual release responsibility ZPD evidence"
  "Gagne nine events of instruction validation"
  "{교수설계 원칙} 학술 근거"
```

### 우선순위별 검색 예산

| 우선순위 | WebSearch 예산/건 | 처리 순서 |
|---------|-----------------|----------|
| 높음 | 4~5회 | 1순위 — 반드시 Triangulate |
| 중간 | 2~3회 | 2순위 — 가능하면 Triangulate |
| 낮음 | 1~2회 | 3순위 — 예산 잔여 시 |

---

## Step 1: deep-research 스킬 지침에 따른 리서치 수행

| 항목 | 내용 |
|------|------|
| 입력 | `deep_research_plan.md`, `.claude/skills/deep-research/SKILL.md` |
| 참조 | `.claude/skills/deep-research/reference/methodology.md` (Phase별 상세) |
| 도구 | Read, Glob, Bash, WebSearch, WebFetch, Write (3자료원 필수) |
| 산출물 | `verification_results.md`, `supplement_results.md` |
| 제약 | 웹 검색 25회 이내, NBLM 쿼리 5회 이내, 삼각검증 추가 5회 이내 |

**동작**:

1. `.claude/skills/deep-research/SKILL.md` 읽기 — 8단계 파이프라인 지침 로드
2. `.claude/skills/deep-research/reference/methodology.md` 읽기 — Phase별 상세 활동 참조
3. `deep_research_plan.md`의 요청을 **우선순위순**(높음 → 중간 → 낮음)으로 처리
4. 각 요청에 대해 deep-research 8단계 파이프라인 수행:

### 1-1. Scope (리서치 범위 정의) — 교안 특화 성공 기준

각 요청을 독립 리서치 단위로 분해:
- 핵심 질문 명확화 (1문장)
- 범위 경계 설정 (포함/제외)
- **교안 특화 성공 기준**:
  - 사례 검증: "효과 크기와 맥락 전이({target_learner}) 근거 확보"
  - 활동 보충: "SLO 적합 템플릿/루브릭/발문 3개 이상 수집"
  - 사실 확인: "3중 소스 일관된 결론 도출"

### 1-2. Plan (검색 전략 수립)

유형별 차별화:
- **사례 검증**: 메타분석 검색 → 대학 CTL 사례 → 교사 커뮤니티 토론
- **활동 보충**: 대학 CTL 템플릿 검색 → 교육공학 저널 → 교사 커뮤니티 자료
- **사실 확인**: 공식 교수설계 문헌 URL 직접 검색 → 논문 → 전문가 블로그

검색어 설계 (한국어 + 영어 병행):
```
사례 검증 예시:
  "{교수법} effectiveness meta-analysis systematic review"
  "{교수법} {대상 학습자} 효과 연구"
  "{활동 전략} classroom evidence"

활동 보충 예시:
  "{SLO 키워드} rubric template"
  "Bloom's {수준} question stems {topic}"
  "{topic} formative assessment examples"

사실 확인 예시:
  "{교수설계 원칙} original source validation"
  "{이론명} empirical evidence review"
  "{원칙} 학술적 근거 검증"
```

### 1-3. Retrieve (3자료원 필수 수집)

3개 자료원을 **모두** 순차 실행한다. Phase 2 산출물(research_exploration.md)을 재활용하는 것이 아니라, **원본 자료를 심화 질문으로 새롭게 분석**하는 독립 과정이다.

**1-3a. 로컬 참고자료 분석 (필수)**

| 항목 | 내용 |
|------|------|
| 입력 | `input_data.json` → `script_config.reference_sources.local_folders` + `deep_research_plan.md` |
| 도구 | Glob, Read, Bash |
| 건너뛰기 조건 | `local_folders`가 빈 배열인 경우에만 건너뜀 (사유 기록) |

동작:
1. `deep_research_plan.md`의 요청별 심화 질문으로 로컬 파일 탐색
2. **파일 읽기**: `shared/file-reading-strategy.md`를 Read하여 확장자별 읽기 전략을 따른다.
3. 요청과 관련된 내용 발견 시 인용 번호 부여 + 발견 내용 기록
4. 관련 내용 미발견 시 "로컬 자료에서 해당 정보 없음" 명시

**1-3b. NotebookLM 쿼리 (필수)**

| 항목 | 내용 |
|------|------|
| 입력 | `input_data.json` → `script_config.reference_sources.notebooklm_urls` + `deep_research_plan.md` |
| 도구 | Bash (NBLM 스킬 CLI) |
| 건너뛰기 조건 | `notebooklm_urls`가 빈 배열인 경우에만 건너뜀 (사유 기록) |
| 제약 | 총 NBLM 쿼리 5회 이내 |

**NBLM 호출**: `shared/nblm-interface.md`를 Read하여 CLI 명령과 후속 질문 프로토콜을 따른다.

동작:
1. `deep_research_plan.md`의 요청을 NBLM 심화 질문으로 변환
2. 우선순위 높은 요청부터 쿼리 예산 배분
3. 쿼리 실행 → 응답에서 관련 팩트 추출 + 인용 번호 부여
4. 관련 내용 미발견 시 "NBLM 소스에서 해당 정보 없음" 명시

**1-3c. 웹 검색 (필수)**

| 항목 | 내용 |
|------|------|
| 도구 | WebSearch, WebFetch |
| 제약 | 총 웹 검색 25회 이내 |

동작:
1. 유형별 검색 전략(사례 검증/활동 보충/사실 확인)에 따라 WebSearch 실행
2. 고품질 소스 선별 → WebFetch로 상세 내용 수집
3. 검색 예산은 우선순위별 배분 (Step 0 계획 참조)

**Anti-Hallucination**: `shared/anti-hallucination.md`를 Read하여 인용 프로토콜을 따른다.

### 1-4. Triangulate (3자료원 교차검증) — 교안 핵심 차별점

`shared/triangulate-rules.md`를 Read하여 기본 교차검증 규칙을 따른다.

3개 자료원(로컬, NBLM, 웹)의 발견을 교차 비교하여 신뢰도를 판정한다.

**교수법 효과성 3중 검증 (교안 Phase 4 신규 — 기본 검증에 추가 적용)**:

| 차원 | 질문 | 적용 유형 | 판정 기준 |
|------|------|----------|----------|
| 효과 크기 | "effect size가 유의미한가? (d≥0.4)" | 사례 검증, 사실 확인 | 메타분석/실험 연구에서 효과 크기 보고 여부 |
| 맥락 전이 | "{target_learner}에게도 적용 가능한가?" | 사례 검증, 활동 보충 | 연구 대상과 target_learner 유사성 비교 |
| SLO 측정 | "이 평가 도구가 해당 SLO를 측정하는가?" | 사실 확인, 활동 보충 | Bloom's 수준 정합성 + 측정 방법 적절성 |

교수법 효과성 검증 결과 태그:
- `[효과성 확인]`: 3차원 중 2+ 충족
- `[효과성 부분 확인]`: 3차원 중 1 충족
- `[효과성 미확인]`: 근거 불충분

### 1-5. Synthesize (통합)

요청별 핵심 발견 통합:
- 사례 검증: 결론 1~2문장 + 효과성 검증 결과 + 상세 근거
- 활동 보충: 수집 자료 목록 + 차시/SLO별 활용 제안
- 사실 확인: 결론 1~2문장 + 이론적 근거 + 3중 소스 일치 상세

### 1-6. Critique (비판적 분석) — 교안 특화 질문 추가

모든 요청에 적용:
- 반대 증거 또는 제한 사항 탐색
- "이 정보가 6개월 후에도 유효한가?" (최신성 검증)
- "이 사례가 {target_learner}에게도 적용 가능한가?" (맥락 전이 재확인)
- **"교수 모델({teaching_model})과 이 전략이 정합적인가?"** (교안 특화)
- **"GRR 단계({grr_focus})에서 이 활동이 적절한가?"** (교안 특화)
- 한계 사항 명시적 문서화

### 1-7. Refine (보완)

Critique에서 발견된 공백 해소:
- 약한 근거 보강 (추가 검색 최대 5회)
- 인용 정확성 최종 확인
- 모순 해결

### 결과 저장 (유형별 분리)

**verification_results.md** (사례 검증 + 사실 확인 요청 결과):
```markdown
### 요청 #{번호}: {요청 내용 요약} [{검증 태그}] [{효과성 태그}]
- 유형: {사례 검증/사실 확인}
- 우선순위: {높음/중간/낮음}
- 관련 차시/SLO: {brainstorm_result.md §7 참조}

#### 결론
{1~2문장 핵심 결론}

#### 교수법 효과성 검증
- 효과 크기: {결과 및 근거}
- 맥락 전이: {target_learner 적용 가능성}
- SLO 측정: {해당 SLO 측정 타당성}

#### 상세 발견
- {팩트 1} [N]
- {팩트 2} [N]
- {팩트 3} [N]

#### 삼각 검증 결과
{소스 간 일치/불일치 상세}

#### 한계/주의사항
{최신성, 맥락 적용 가능성, 반대 증거, 교수 모델 정합성}

#### 소스
| # | URL/경로 | 자료원 | 유형 | 접근일자 | 신뢰도 |
(자료원: 로컬/NBLM/웹)
```

**supplement_results.md** (활동 보충 요청 결과):
```markdown
### 요청 #{번호}: {요청 내용 요약}
- 유형: 활동 보충
- 우선순위: {높음/중간/낮음}
- 관련 차시/SLO: {brainstorm_result.md §7 참조}

#### 수집 자료
- {루브릭/발문/활동 템플릿/훅 소재 1} [N]
- {루브릭/발문/활동 템플릿/훅 소재 2} [N]

#### 차시/SLO별 활용 제안
{어떤 차시의 어떤 SLO에서, GRR 어떤 단계에, 어떻게 활용할 수 있는지}

#### 한계/주의사항
{적용 시 고려할 점, target_learner 맥락 전이 가능성}

#### 소스
| # | URL/경로 | 자료원 | 유형 | 접근일자 | 신뢰도 |
(자료원: 로컬/NBLM/웹)
```

---

## Step 2: 출력 정규화 + Phase 5·6 전달용 통합

| 항목 | 내용 |
|------|------|
| 입력 | `verification_results.md`, `supplement_results.md`, `brainstorm_result.md` |
| 도구 | Read, Write |
| 산출물 | `{output_dir}/research_deep.md` ★ 최종 산출물 |

**동작**:

1. 검증/보충 결과를 요청 번호순으로 정렬
2. Phase 5·6 전달용 **통합 시사점** 3가지 카테고리 분류:
   - **확정된 전제** → architecture-agent(Phase 5)용: 교수법/활동 전략 설계 기반
   - **확보된 소재** → writer-agent(Phase 6)용: 루브릭/발문/활동 템플릿/훅 소재
   - **미해결 항목** → 대안 마련 또는 강사 확인 필요
3. `research_deep.md` 작성 (아래 산출물 구조)

### research_deep.md 산출물 구조 (교안 전용)

```markdown
# 심화 리서치 결과 (교안)

## 메타데이터
- 강의 주제: {topic}
- 교수 모델: {teaching_model}
- 리서치 일자: {date}
- 리서치 방법론: deep-research 스킬 8단계 파이프라인
- 실행 모드: {Standard/Deep}
- 요청 처리 현황: 총 {N}건 (사례 검증 {N}건, 활동 보충 {N}건, 사실 확인 {N}건)
- 검색 통계: 웹 {N}회, 로컬 재조회 {N}건, NBLM 재쿼리 {N}회
- 입력 소스: brainstorm_result.md §7

---

## 1. 검증 결과 (Verification)

### 요청 #1: {요청 내용 요약} [확정/높은 확신/불일치/미검증] [효과성 확인/부분 확인/미확인]
- 관련 차시/SLO: {brainstorm_result.md §7 참조}
- 우선순위: {높음/중간/낮음}

**결론**: {1~2문장 핵심 결론}

**교수법 효과성 검증**:
- 효과 크기: {결과}
- 맥락 전이: {결과}
- SLO 측정: {결과}

**상세 발견**:
- {팩트 1} [1]
- {팩트 2} [2]
- {팩트 3} [3]

**삼각 검증 결과**: {소스 간 일치/불일치 상세}

**한계/주의사항**: {최신성, 맥락 적용 가능성, 반대 증거, 교수 모델 정합성}

(사례 검증/사실 확인 요청별 반복)

---

## 2. 보충 자료 (Supplement)

### 요청 #N: {요청 내용 요약}
- 관련 차시/SLO: {brainstorm_result.md §7 참조}
- 우선순위: {높음/중간/낮음}

**수집 자료**:
- {루브릭/발문/활동 템플릿/훅 소재 1} [N]
- {루브릭/발문/활동 템플릿/훅 소재 2} [N]

**차시/SLO별 활용 제안**: {어떤 차시의 어떤 SLO에서 어떻게 활용할 수 있는지}

**한계/주의사항**: {적용 시 고려할 점}

(활동 보충 요청별 반복)

---

## 3. 통합 시사점

### 3-1. 확정된 전제 (Confirmed Premises) → Phase 5 architecture-agent용
{검증 통과한 교수법/활동 전략 — 교안 구조 설계에서 안심하고 반영 가능}
- {전제 1}: {근거 요약} [확정]
- {전제 2}: {근거 요약} [확정]

### 3-2. 확보된 소재 (Collected Materials) → Phase 6 writer-agent용
{보충 수집된 루브릭/발문/활동 템플릿/훅 소재 — 교안 대본에서 직접 참조 가능}
- {소재 1}: {활용 방안 — 차시, SLO, GRR 단계}
- {소재 2}: {활용 방안 — 차시, SLO, GRR 단계}

### 3-3. 미해결 항목 (Unresolved Items)
{검증 실패 또는 불충분 — 대안 마련 또는 강사 확인 필요}
- {항목 1}: {상태 + 권장 대응}

---

## 출처 목록

| # | 출처 | 자료원 | 유형 | 접근일자 | 신뢰도 |
|---|------|--------|------|---------|--------|
| [1] | {URL/파일경로} | 로컬/NBLM/웹 | 사례검증/활동보충/사실확인 | {날짜} | [확정/높은 확신/미검증] |
```
