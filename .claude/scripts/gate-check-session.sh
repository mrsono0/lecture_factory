#!/bin/bash
# gate-check-session.sh — session 파일의 정량 검증
# 사용법: gate-check-session.sh <session_file> <content_type> [subtype]
# content_type: hands-on / concept / activity
# subtype (선택): setup — 설치·환경 구성 성격 차시의 추가 검증
# 반환: 0=PASS, 1=FAIL (FAIL 시 원인을 stdout 출력)

set -euo pipefail

SESSION_FILE="${1:?사용법: gate-check-session.sh <session_file> <content_type> [subtype]}"
CONTENT_TYPE="${2:?content_type 필요: hands-on / concept / activity}"
SUBTYPE="${3:-}"

FAIL=0
REASONS=""

add_fail() {
  FAIL=1
  REASONS="${REASONS}FAIL: $1\n"
}

# ── 1. 금지 문구 검출 ──
FORBIDDEN_PATTERNS=(
  "구성안 비유 체계 참조"
  "선수 확인 질문"
  "강사 시연을 따라 코드 작성"
  "다음 차시 주제와의 연결점을 안내합니다"
  "해당 SLO 달성 여부 확인"
)

for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  count=$(grep -c "$pattern" "$SESSION_FILE" 2>/dev/null || true)
  if [ "$count" -gt 0 ]; then
    add_fail "금지 문구 발견: \"$pattern\" (${count}회)"
  fi
done

# ── 2. 줄 수 하한 ──
LINE_COUNT=$(wc -l < "$SESSION_FILE" | tr -d ' ')

case "$CONTENT_TYPE" in
  hands-on)
    MIN_LINES=150
    ;;
  concept)
    MIN_LINES=120
    ;;
  activity)
    MIN_LINES=100
    ;;
  *)
    MIN_LINES=100
    ;;
esac

if [ "$LINE_COUNT" -lt "$MIN_LINES" ]; then
  add_fail "줄 수 부족: ${LINE_COUNT}줄 (최소 ${MIN_LINES}줄, content_type=${CONTENT_TYPE})"
fi

# ── 3. 코드 블록 카운트 (hands-on 차시) ──
CODE_FENCE_COUNT=$(grep -c '```' "$SESSION_FILE" 2>/dev/null || true)

if [ "$CONTENT_TYPE" = "hands-on" ]; then
  # 코드 블록 열기+닫기 = 쌍. 최소 3쌍(6개) 필요 (I Do + We Do + You Do)
  if [ "$CODE_FENCE_COUNT" -lt 6 ]; then
    add_fail "hands-on 코드 블록 부족: ${CODE_FENCE_COUNT}개 fence (최소 6개 = 3쌍)"
  fi
fi

# ── 4. ★ 핵심 예시 마커 카운트 ──
STAR_COUNT=$(grep -c '★' "$SESSION_FILE" 2>/dev/null || true)

if [ "$CONTENT_TYPE" = "hands-on" ] || [ "$CONTENT_TYPE" = "concept" ]; then
  if [ "$STAR_COUNT" -lt 2 ]; then
    add_fail "★ 핵심 예시 부족: ${STAR_COUNT}개 (최소 2개)"
  fi
fi

# ── 5. 동일 흔한 실수 패턴 검출 ──
GENERIC_MISTAKE=$(grep -c "어노테이션 누락" "$SESSION_FILE" 2>/dev/null || true)
if [ "$GENERIC_MISTAKE" -gt 0 ]; then
  # 추가 확인: "패키지 위치 오류"도 동시에 있으면 템플릿 복사로 판단
  GENERIC_MISTAKE2=$(grep -c "패키지 위치 오류" "$SESSION_FILE" 2>/dev/null || true)
  if [ "$GENERIC_MISTAKE2" -gt 0 ]; then
    add_fail "흔한 실수 시나리오가 범용 템플릿 (어노테이션 누락 + 패키지 위치 오류)"
  fi
fi

# ── 6. setup subtype 전용 검증 ──
if [ "$SUBTYPE" = "setup" ]; then
  # URL/다운로드 경로 존재 확인
  URL_COUNT=$(grep -cE 'https?://' "$SESSION_FILE" 2>/dev/null || true)
  if [ "$URL_COUNT" -lt 1 ]; then
    add_fail "setup 차시: URL/다운로드 경로 없음 (최소 1개 필요)"
  fi

  # 명령어 예상 출력/결과 확인
  EXPECTED_COUNT=$(grep -c '예상 출력\|예상 결과' "$SESSION_FILE" 2>/dev/null || true)
  if [ "$EXPECTED_COUNT" -lt 1 ]; then
    add_fail "setup 차시: 명령어 예상 출력/결과 없음 (최소 1개 필요)"
  fi

  # 단계별 설치 과정 (번호 매긴 단계 4개 이상)
  STEP_COUNT=$(grep -cE '^\*\*[0-9]+단계' "$SESSION_FILE" 2>/dev/null || true)
  if [ "$STEP_COUNT" -lt 4 ]; then
    add_fail "setup 차시: 단계별 설치 과정 부족 (${STEP_COUNT}단계, 최소 4단계 필요)"
  fi
fi

# ── 7. I Do 핵심개념 섹션 줄 수 ──
# "### 핵심 개념" ~ 다음 "###" 사이의 줄 수 계산
CORE_LINES=$(sed -n '/^### 핵심 개념/,/^### /{/^### 핵심 개념/d;/^###/d;p;}' \
  "$SESSION_FILE" | wc -l | tr -d ' ')

if [ "$SUBTYPE" = "setup" ]; then
  MIN_CORE=15
else
  case "$CONTENT_TYPE" in
    hands-on) MIN_CORE=8 ;;
    concept)  MIN_CORE=8 ;;
    *)        MIN_CORE=5 ;;
  esac
fi

if [ "$CORE_LINES" -lt "$MIN_CORE" ]; then
  add_fail "핵심개념 섹션 줄 수 부족: ${CORE_LINES}줄 (최소 ${MIN_CORE}줄, type=${CONTENT_TYPE}, subtype=${SUBTYPE:-none})"
fi

# ── 8. 오개념 교정 테이블 실제 데이터 행 ──
# "### 오개념 교정" 이후 테이블에서 헤더/구분선 제외한 데이터 행 카운트
MISCONCEPTION_ROWS=$(sed -n '/^### 오개념 교정/,/^## /{/^|/p;}' "$SESSION_FILE" \
  | grep -v '^\s*|.*---' | grep -v '오개념.*올바른 이해.*교정' | wc -l | tr -d ' ')

if [ "$MISCONCEPTION_ROWS" -lt 1 ]; then
  add_fail "오개념 교정 테이블에 실제 데이터 행 없음 (최소 1행 필요)"
fi

# ── 결과 출력 ──
SUBTYPE_LABEL=""
if [ -n "$SUBTYPE" ]; then
  SUBTYPE_LABEL=", subtype=${SUBTYPE}"
fi

if [ "$FAIL" -eq 0 ]; then
  echo "PASS: ${SESSION_FILE} (${LINE_COUNT}줄, 코드블록=${CODE_FENCE_COUNT}, ★=${STAR_COUNT}, 핵심개념=${CORE_LINES}줄, 오개념행=${MISCONCEPTION_ROWS}${SUBTYPE_LABEL})"
  exit 0
else
  echo "=== GATE-6 FAIL: ${SESSION_FILE} ==="
  echo -e "$REASONS"
  exit 1
fi
