"""Режим разработки с MCP и подпиской Claude (п. 4.5.3 ТЗ).

Здесь будет MCP-сервер с инструментами list_llm_tasks, get_llm_task,
submit_llm_result, run_synthetic_interview, run_analysis, get_dashboard_json.
Сервер запускается только при DEV_MODE=true и работает только
с синтетическими и тестовыми данными.
"""
