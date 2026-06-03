"""Experiment configuration — API keys loaded from environment variables"""
import os

CONFIGS = {
    "deepseek": {
        "base_url": os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/anthropic"),
        "api_key": os.environ.get("DEEPSEEK_API_KEY", ""),
        "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
    },
    "mimo": {
        "base_url": os.environ.get("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/anthropic"),
        "api_key": os.environ.get("MIMO_API_KEY", ""),
        "model": os.environ.get("MIMO_MODEL", "mimo-v2.5-pro"),
    },
}

def get_config(provider=None):
    if provider is None:
        provider = os.environ.get("LLM_PROVIDER", "deepseek")
    cfg = CONFIGS[provider]
    if not cfg["api_key"]:
        raise ValueError(f"Please set {provider.upper()}_API_KEY environment variable")
    return cfg
