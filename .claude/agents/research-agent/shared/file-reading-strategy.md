# 파일 읽기 전략 (확장자별)

## 확장자별 읽기 방법

| 확장자 | 읽기 방법 | 비고 |
|--------|----------|------|
| `.md` `.txt` | Read 도구 직접 읽기 | |
| `.pdf` (≤20p) | `Read(pages="1-20")` | Read 도구 내장 PDF 지원 (1순위) |
| `.pdf` (>20p) | `Bash: /opt/homebrew/bin/pdftotext "{file}" -` | poppler 26.03 설치됨 |
| `.pdf` (Read 실패 시) | `Bash: source .venv/bin/activate && python -c "import pdfplumber; ..."` | pdfplumber 0.11.9 설치됨 |
| `.pptx` | `Bash: source .venv/bin/activate && python -c "..."` (아래 스크립트) | python-pptx 설치 시 |
| `.docx` | `Bash: pandoc {file} -t plain` | pandoc 설치 시 |

## PPTX 읽기 인라인 스크립트

```bash
source .venv/bin/activate && python -c "
from pptx import Presentation; import sys
prs = Presentation(sys.argv[1])
for i, slide in enumerate(prs.slides, 1):
    title = slide.shapes.title.text if slide.shapes.title else '(제목 없음)'
    body = ' '.join(s.text for s in slide.shapes if hasattr(s,'text') and s != slide.shapes.title)
    print(f'## 슬라이드 {i}: {title}')
    if body.strip(): print(body[:500])
    print()
" "{파일경로}"
```

## PDF 읽기 인라인 스크립트 (pdfplumber 폴백)

```bash
source .venv/bin/activate && python -c "
import pdfplumber, sys
pdf = pdfplumber.open(sys.argv[1])
for i, page in enumerate(pdf.pages, 1):
    text = page.extract_text()
    if text:
        print(f'--- Page {i} ---')
        print(text)
pdf.close()
" "{파일경로}"
```

## 파일 선별 규칙

- 각 로컬 폴더에 `Glob("**/*.{md,txt,pdf,pptx,docx}")` 실행
- 파일 10개 초과 시 파일명/크기 기준 우선순위 선별
- 확장자별 분기로 읽기 실행
