"""
pytest 共享配置
所有测试文件共享的 fixture 和配置
"""
import os
import pytest
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


def pytest_configure(config):
    """配置 SiliconFlow API"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        raise pytest.skip(
            "未找到 SILICONFLOW_API_KEY 环境变量，跳过测试。\n"
            "请复制 .env.example 为 .env 并填入你的 API Key。"
        )

    # 设置 DeepEval 使用的 OpenAI 兼容接口
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"


@pytest.fixture
def eval_model():
    """默认评测模型"""
    return "deepseek-ai/DeepSeek-V3"


@pytest.fixture
def sample_context():
    """示例上下文数据"""
    return [
        "Python 是一种高级编程语言，由 Guido van Rossum 于1991年创建。",
        "Python 的设计哲学强调代码的可读性和简洁性。",
        "Python 支持多种编程范式，包括面向对象、函数式和过程式编程。"
    ]