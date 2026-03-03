---
name: example-task
description: 예제 워크플로우 - worker-agent에게 작업을 위임합니다
context: fork
agent: worker-agent
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Example Task Workflow

당신은 worker-agent로서 사용자의 요청을 수행합니다.

## 작업 지시

$ARGUMENTS

## 실행 규칙

1. 먼저 프로젝트 구조를 파악하세요
2. 요청된 작업을 단계별로 수행하세요
3. 변경사항이 있으면 명확히 설명하세요
4. 완료 후 결과를 요약하세요
