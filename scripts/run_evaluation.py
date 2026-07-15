"""
批量评测脚本 - 从 JSON 文件加载测试数据
每个用例只评测对应的指标，避免交叉误判
"""
import os
import json
import time
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase


def load_json_data(filepath: str) -> dict:
    """加载 JSON 数据文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_context_by_id(contexts_data: dict, context_id: str) -> list:
    """根据 ID 获取上下文内容"""
    for ctx in contexts_data.get("contexts", []):
        if ctx["id"] == context_id:
            return ctx["content"]
    return []


def get_metric_by_category(category: str, model: str):
    """根据 category 返回对应的评测指标"""
    metric_map = {
        "faithfulness": [FaithfulnessMetric(threshold=0.7, model=model)],
        "hallucination": [HallucinationMetric(threshold=0.5, model=model)],
        "answer_relevancy": [AnswerRelevancyMetric(threshold=0.7, model=model)],
        "contextual_relevancy": [FaithfulnessMetric(threshold=0.6, model=model)],
        "multi_metric": [
            FaithfulnessMetric(threshold=0.7, model=model),
            AnswerRelevancyMetric(threshold=0.7, model=model),
        ]
    }
    return metric_map.get(category, [FaithfulnessMetric(threshold=0.7, model=model)])


def build_test_case(item: dict, context: list) -> LLMTestCase:
    """根据 category 构建正确的测试用例"""
    kwargs = {
        "input": item["input"],
        "actual_output": item["actual_output"],
    }

    # HallucinationMetric 需要 context
    # FaithfulnessMetric 需要 retrieval_context
    category = item.get("category", "")
    if category == "hallucination":
        kwargs["context"] = context
    else:
        kwargs["retrieval_context"] = context

    return LLMTestCase(**kwargs)


def main():
    # 配置 API
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 SILICONFLOW_API_KEY 环境变量")
        print("请复制 .env.example 为 .env 并填入你的 API Key")
        return

    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"

    # 模型选择（白天用 DeepSeek-V3，限流时换本地 qwen:1.8b）
    MODEL = "deepseek-ai/DeepSeek-V3"
    # MODEL = "qwen:1.8b"  # 本地 Ollama 备用

    print("📂 加载测试数据...")
    contexts_data = load_json_data("data/sample_contexts.json")
    questions_data = load_json_data("data/test_questions.json")

    print(f"📝 准备 {len(questions_data['test_cases'])} 个测试用例...")
    print(f"🤖 使用模型: {MODEL}")

    passed = 0
    failed = 0

    print(f"\n🚀 开始逐个评测...")
    print("=" * 70)

    for i, item in enumerate(questions_data["test_cases"]):
        # 获取上下文
        context = []
        if "context_id" in item:
            context = load_context_by_id(contexts_data, item["context_id"])

        # 构建测试用例（根据 category 选择正确参数）
        test_case = build_test_case(item, context)

        # 获取对应指标
        metrics = get_metric_by_category(item["category"], MODEL)

        print(f"\n🎯 用例 {i + 1}/{len(questions_data['test_cases'])} [{item['id']}]")
        print(f"   类别: {item['category']} | 类型: {item['type']}")
        print(f"   问题: {item['input']}")
        print(f"   回答: {item['actual_output'][:60]}...")

        try:
            assert_test(test_case, metrics)
            status = "✅ 通过"
            passed += 1
        except AssertionError as e:
            status = "❌ 失败"
            failed += 1
            # 提取失败原因
            error_msg = str(e)
            if "reason:" in error_msg:
                reason = error_msg.split("reason:")[-1].strip()[:80]
                print(f"   原因: {reason}...")

        expected = "预期通过" if item["expected_result"] == "pass" else "预期失败"
        print(f"   结果: {status} ({expected})")

        # 间隔 2 秒，避免限流
        if i < len(questions_data["test_cases"]) - 1:
            time.sleep(2)

    print(f"\n{'=' * 70}")
    print(f"📊 评测报告")
    print(f"{'=' * 70}")
    print(f"📈 总计: {passed} 通过, {failed} 失败")

    # 统计符合预期的数量
    correct = 0
    for item in questions_data["test_cases"]:
        # 这里简化处理，实际应该记录每个用例的结果
        pass

    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()