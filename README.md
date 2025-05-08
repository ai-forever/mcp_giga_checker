# MCP Giga Checker

MCP Giga Checker — это сервер MCP (Model Context Protocol) для проверки текста на сгенерированность искусственным интеллектом через GigaChat API от Сбера.

Сервер предоставляет интеграцию проверки сгенерированности текста в ваших ИИ-ассистентов.

## Возможности
- Проверка текста на признаки генерации ИИ (GigaChat)
- Готовность к работе с агентами на базе MCP (например, Cursor)

## Требования
- Python 3.12+
- Доступ к GigaChat API (см. тарифы ниже)

## Установка


## Запуск MCP-сервера


Добавьте сервер в ваш `json`-конфигурационный файл:

```json
"mcpServers": {
  "mcp-giga-checker": {
    "command": "uvx",
    "args": ["--from", "mcp_giga_checker", "mcp-giga-checker"],
    "enabled": true,
    "env": {
      "GIGACHAT_AUTH": "ваши_авторизационные_данные_GigaChat",
      "GIGACHAT_SCOPE": "GIGACHAT_API_CORP"
    }
  }
}
```

## Важно: тарифы GigaChat API

Проверка сгенерированности текста через GigaChat API доступна только для пользователей с корпоративным доступом (тарифы для юрлиц). Подробнее: [Тарифы GigaChat API для юрлиц](https://developers.sber.ru/docs/ru/gigachat/tariffs/legal-tariffs)

## Лицензия

MIT  



