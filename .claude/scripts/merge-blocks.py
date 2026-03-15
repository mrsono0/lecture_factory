#!/usr/bin/env python3
"""Phase 10 블록 병합 스크립트 — session + narration GRR 인터리빙.

사용법:
    python3 .claude/scripts/merge-blocks.py {output_dir} [블록ID|all]

예시:
    python3 .claude/scripts/merge-blocks.py lectures/2026-03-14_.../02_script all
    python3 .claude/scripts/merge-blocks.py lectures/2026-03-14_.../02_script D1_AM

[CRITICAL] LLM 에이전트(worker-agent)로 병합하지 않는다.
블록 병합은 텍스트 구조 변환이며 블록당 입력이 90~170KB로
에이전트의 출력 토큰 한계를 초과한다. 반드시 이 스크립트로 실행한다.
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# GRR 섹션 파싱 패턴
# ---------------------------------------------------------------------------

SESSION_HEADINGS = [
    ("도입",      re.compile(r"^## 도입")),
    ("I Do",     re.compile(r"^## I Do")),
    ("We Do",    re.compile(r"^## We Do")),
    ("You Do",   re.compile(r"^## You Do")),
    ("정리",      re.compile(r"^## 정리")),
    ("필요 자료",  re.compile(r"^## 필요 자료")),
]

NARR_HEADINGS = [
    ("도입",      re.compile(r"^#{2,3} 도입")),
    ("전개",      re.compile(r"^#{2,3} 전개")),
    ("I Do",     re.compile(r"^#{2,3} I Do")),
    ("We Do",    re.compile(r"^#{2,3} We Do")),
    ("You Do",   re.compile(r"^#{2,3} You Do")),
    ("정리",      re.compile(r"^#{2,3} 정리")),
]

# 비표준 헤딩 → GRR 구간 폴백 매핑
NARR_FALLBACK_HEADINGS = [
    ("You Do",   re.compile(r"^#{2,3} (발표 진행|발표|실습 진행|활동)")),
    ("I Do",     re.compile(r"^#{2,3} (리뷰 가이드|시범)")),
]

# 섹션명 → 🎤 라벨
GRR_LABELS = {
    "도입":    "도입 대본",
    "I Do":   "I Do 대본",
    "We Do":  "We Do 대본",
    "You Do": "You Do 대본",
    "정리":    "정리 대본",
}

# ---------------------------------------------------------------------------
# 유틸리티
# ---------------------------------------------------------------------------

def split_sections(text: str, headings: list, fallbacks: list | None = None) -> dict[str, str]:
    """텍스트를 섹션별로 분할. fallbacks가 있으면 추가 매칭."""
    all_headings = list(headings) + (fallbacks or [])
    lines = text.split("\n")
    sections: dict[str, list[str]] = {}
    cur = "_header"
    buf: list[str] = []

    for line in lines:
        matched = False
        for name, pat in all_headings:
            if pat.match(line):
                if buf:
                    sections.setdefault(cur, []).extend(buf)
                cur = name
                buf = [line]
                matched = True
                break
        if not matched:
            buf.append(line)

    if buf:
        sections.setdefault(cur, []).extend(buf)

    return {k: "\n".join(v) for k, v in sections.items()}


def to_blockquote(text: str) -> str:
    """텍스트를 blockquote(> ) 형식으로 변환."""
    out = []
    for line in text.split("\n"):
        if line.strip():
            out.append(line if line.startswith(">") else f"> {line}")
        else:
            out.append(">")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 블록 구성 (session 파일에서 동적 파싱)
# ---------------------------------------------------------------------------

def discover_blocks(output_dir: Path) -> dict[str, dict]:
    """session_D*.md 파일에서 블록 구성을 동적으로 생성."""
    session_files = sorted(output_dir.glob("session_D*.md"))
    if not session_files:
        print(f"ERROR: {output_dir}에 session_D*.md 파일이 없습니다.")
        sys.exit(1)

    # 세션 ID 추출: session_D1-1.md → D1-1
    sids = [f.stem.replace("session_", "") for f in session_files]

    # Day별 그룹핑
    days: dict[int, list[str]] = defaultdict(list)
    for sid in sids:
        day = int(sid[1])
        days[day].append(sid)

    # Day 테마 (기본값 — architecture.md에서 파싱 가능하면 덮어쓰기)
    themes = {1: "출발", 2: "구조", 3: "데이터", 4: "품질", 5: "완성"}
    arch_file = output_dir / "architecture.md"
    if arch_file.exists():
        arch_text = arch_file.read_text("utf-8")
        for m in re.finditer(r"Day (\d).*?[:：]\s*(.+?)[\s—\-]", arch_text):
            themes[int(m.group(1))] = m.group(2).strip()

    # AM/PM 분할 (sessions_in_day ≥ 6이면 분할)
    blocks: dict[str, dict] = {}
    for day, day_sids in sorted(days.items()):
        theme = themes.get(day, "")
        if len(day_sids) >= 6:
            mid = len(day_sids) // 2
            blocks[f"D{day}_AM"] = {
                "day": day, "half": "오전", "theme": theme,
                "sessions": day_sids[:mid],
            }
            blocks[f"D{day}_PM"] = {
                "day": day, "half": "오후", "theme": theme,
                "sessions": day_sids[mid:],
            }
        else:
            blocks[f"D{day}"] = {
                "day": day, "half": "전체", "theme": theme,
                "sessions": day_sids,
            }

    return blocks


# ---------------------------------------------------------------------------
# 병합 로직
# ---------------------------------------------------------------------------

def merge_one_session(output_dir: Path, sid: str) -> str:
    """하나의 세션에 대해 session + narration 인터리빙."""
    sf = output_dir / f"session_{sid}.md"
    nf = output_dir / f"narration_{sid}.md"

    if not sf.exists():
        return f"# {sid}: [session 파일 없음]\n"

    ss = split_sections(sf.read_text("utf-8"), SESSION_HEADINGS)
    ns = (
        split_sections(nf.read_text("utf-8"), NARR_HEADINGS, NARR_FALLBACK_HEADINGS)
        if nf.exists()
        else {}
    )

    parts: list[str] = []

    # 헤더 (메타데이터 등)
    if "_header" in ss:
        parts.append(ss["_header"])

    # GRR 구간별 인터리빙
    grr_order = ["도입", "I Do", "We Do", "You Do", "정리"]

    for g in grr_order:
        if g not in ss:
            continue

        # 교안 섹션
        parts.append(ss[g])

        # 대본 매칭 (직접 → 폴백)
        narr = ns.get(g)
        if not narr and g == "I Do" and "전개" in ns:
            narr = ns["전개"]

        if narr:
            label = GRR_LABELS.get(g, f"{g} 대본")
            parts.append(f"\n> 🎤 **{label}**")
            parts.append(to_blockquote(narr))

        parts.append("\n---\n")

    # 필요 자료
    if "필요 자료" in ss:
        parts.append(ss["필요 자료"])

    return "\n".join(parts)


def merge_block(output_dir: Path, bid: str, info: dict) -> None:
    """하나의 블록 파일 생성."""
    header = f"# Block {bid} — Day {info['day']}: {info['theme']} ({info['half']})\n\n"
    content = [header]

    for sid in info["sessions"]:
        content.append(f"\n{'=' * 60}\n")
        content.append(merge_one_session(output_dir, sid))

    out_file = output_dir / f"block_{bid}.md"
    out_file.write_text("\n".join(content), "utf-8")

    # 검증 출력
    txt = out_file.read_text("utf-8")
    mic = txt.count("🎤")
    ln = len(txt.split("\n"))
    sessions = len(info["sessions"])
    expected_min = int(sessions * 4 * 0.8)
    status = "✅" if mic >= expected_min else "⚠️"
    print(f"{status} {bid}: {ln}줄, 🎤={mic} (기대≥{expected_min})")


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("사용법: python3 merge-blocks.py {output_dir} [블록ID|all]")
        print("예시:   python3 merge-blocks.py lectures/.../02_script all")
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    if not output_dir.is_dir():
        print(f"ERROR: 디렉토리가 존재하지 않습니다: {output_dir}")
        sys.exit(1)

    target = sys.argv[2] if len(sys.argv) > 2 else "all"
    blocks = discover_blocks(output_dir)

    if target == "all":
        for bid, info in blocks.items():
            merge_block(output_dir, bid, info)
    elif target in blocks:
        merge_block(output_dir, target, blocks[target])
    else:
        print(f"ERROR: 알 수 없는 블록 ID: {target}")
        print(f"사용 가능: {', '.join(blocks.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
