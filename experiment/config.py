"""实验配置"""
import os

# API配置（通过环境变量或直接修改）
CONFIGS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com/anthropic",
        "api_key": "REDACTED",
        "model": "deepseek-chat",
    },
    "mimo": {
        "base_url": "https://token-plan-cn.xiaomimimo.com/anthropic",
        "api_key": "REDACTED",
        "model": "mimo-v2.5-pro",
    },
}

def get_config(provider=None):
    if provider is None:
        provider = os.environ.get("LLM_PROVIDER", "deepseek")
    return CONFIGS[provider]
