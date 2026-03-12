# NotebookLM (NBLM) 호출 인터페이스

## CLI 명령

```bash
# 1. 노트북 활성화 (URL 또는 ID)
python3 .claude/skills/nblm/scripts/run.py nblm_cli.py activate {url}

# 2. 질문 (각 질문은 독립 컨텍스트)
python3 .claude/skills/nblm/scripts/run.py ask_question.py --question "{질문}"
```

## 제약

- 노트북당 최대 5쿼리 (일일 50쿼리 제한 고려)

## 후속 질문 프로토콜

NBLM 응답 끝에 "Is that ALL you need to know?" 수신 시:
- 원래 리서치 질문 대비 정보 충분성 판단
- 부족하면 추가 쿼리 실행 (쿼리 예산 내)
- 충분하면 다음 단계로 진행
