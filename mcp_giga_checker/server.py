from mcp.server.fastmcp import FastMCP
import os
import httpx
import uuid
import asyncio
import ssl

print("SSL default verify paths:", ssl.get_default_verify_paths())
print("SSL env:", {k: v for k, v in os.environ.items() if 'SSL' in k or 'CA' in k})

mcp = FastMCP("mcp_giga_checker")

GIGACHAT_AUTH_ENV = "GIGACHAT_AUTH"
GIGACHAT_SCOPE_ENV = "GIGACHAT_SCOPE"

# Глобальный SSLContext с отключённой проверкой
_unverified_ctx = ssl.create_default_context()
_unverified_ctx.check_hostname = False
_unverified_ctx.verify_mode = ssl.CERT_NONE

async def get_access_token() -> str:
    """
    Получает access_token для GigaChat API, используя переменные окружения GIGACHAT_AUTH (ключ авторизации, base64) и GIGACHAT_SCOPE.
    """
    auth = os.getenv(GIGACHAT_AUTH_ENV)
    if not auth:
        raise ValueError(f"Environment variable {GIGACHAT_AUTH_ENV} not set")
    scope = os.getenv(GIGACHAT_SCOPE_ENV)
    if not scope:
        raise ValueError(f"Environment variable {GIGACHAT_SCOPE_ENV} not set")
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth}",
    }
    data = {"scope": scope}
    print("[DEBUG] Requesting access token with headers:", headers)
    async with httpx.AsyncClient(verify=_unverified_ctx, trust_env=False) as client:
        resp = await client.post(url, headers=headers, data=data)
        print("[DEBUG] Access token response status:", resp.status_code)
        resp.raise_for_status()
        token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("Failed to obtain access token from GigaChat OAuth API")
    return token

@mcp.tool()
async def giga_check_text(input: str, model: str = "GigaCheckDetection") -> dict:
    """
    Проверяет, написан ли текст с помощью ИИ через эндпоинт GigaChat /ai/check.
    Токен всегда получается автоматически.
    """
    access_token = await get_access_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/ai/check"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
    }
    payload = {"input": input, "model": model}
    print("[DEBUG] Sending AI check request with headers:", headers)
    async with httpx.AsyncClient(verify=_unverified_ctx, trust_env=False) as client:
        resp = await client.post(url, headers=headers, json=payload)
        print("[DEBUG] AI check response status:", resp.status_code)
        resp.raise_for_status()
        return resp.json()

@mcp.tool()
async def giga_check_file(file_path: str, model: str = "GigaCheckDetection") -> dict:
    """
    Проверяет, написан ли текстовый файл с помощью ИИ через эндпоинт GigaChat /ai/check.
    Токен всегда получается автоматически.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return await giga_check_text(text, model=model)

def run():
    mcp.run(transport="stdio") 