# Planner Prompt
ProjectBrief를 Task tree로 분해하고 첫 번째 실행 task를 우선 반환하라.

## Output JSON Schema
{
  "tasks": [
    {
      "task_id": "string",
      "title": "string",
      "description": "string"
    }
  ]
}
