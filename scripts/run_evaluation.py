"""
批量评测脚本 - 从 JSON 文件加载测试数据
"""
import os
import json
from deepeval import evaluate
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


def main():
    # 确保 API Key 已设置
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 SILICONFLOW_API_KEY 环境变量")
        print("请复制 .env.example 为 .env 并填入你的 API Key")
        return

    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"

    # 加载数据
    print("📂 加载测试数据...")
    contexts_data = load_json_data("data/sample_contexts.json")
    questions_data = load_json_data("data/test_questions.json")

    # 构建测试用例
    test_cases = []
    print(f"📝 构建 {len(questions_data['test_cases'])} 个测试用例...")

    for item in questions_data["test_cases"]:
        # 获取上下文
        context = []
        if "context_id" in item:
            context = load_context_by_id(contexts_data, item["context_id"])

        # 构建测试用例
        test_case = LLMTestCase(
            input=item["input"],
            actual_output=item["actual_output"],
            context=context if item["category"] in ["hallucination"] else None,
            retrieval_context=context if item["category"] in ["faithfulness", "contextual_relevancy"] else None
        )
        test_cases.append(test_case)

    # 定义评测指标
    metrics = [
        FaithfulnessMetric(threshold=0.7, model="deepseek-ai/DeepSeek-V3"),
        AnswerRelevancyMetric(threshold=0.7, model="deepseek-ai/DeepSeek-V3"),
        HallucinationMetric(threshold=0.5, model="deepseek-ai/DeepSeek-V3")
    ]

    # 运行批量评测
    print(f"\n🚀 开始评测 {len(test_cases)} 个测试用例...")
    print("=" * 60)
    results = evaluate(test_cases=test_cases, metrics=metrics)

    # 打印结果摘要
    print("\n" + "=" * 60)
    print("📊 评测报告")
    print("=" * 60)

    passed = 0
    failed = 0

    for i, (result, item) in enumerate(zip(results.test_results, questions_data["test_cases"])):
        status = "✅ 通过" if result.success else "❌ 失败"
        expected = "预期通过" if item["expected_result"] == "pass" else "预期失败"

        print(f"\n用例 {i+1} [{item['id']}]: {status} ({expected})")
        print(f"  类别: {item['category']} | 类型: {item['type']}")
        print(f"  问题: {item['input']}")
        print(f"  回答: {item['actual_output'][:80]}...")

        for metric in result.metrics_data:
            emoji = "✅" if metric.score >= metric.threshold else "❌"
            print(f"  {emoji} {metric.name}: {metric.score:.2f} (阈值: {metric.threshold})")
            if metric.reason:
                print(f"      原因: {metric.reason[:100]}...")

        if result.success:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"📈 总计: {passed} 通过, {failed} 失败")
    print(f"✅ 符合预期的通过: {sum(1 for t, r in zip(questions_data['test_cases'], results.test_results) if t['expected_result'] == 'pass' and r.success)}")
    print(f"✅ 符合预期的失败: {sum(1 for t, r in zip(questions_data['test_cases'], results.test_results) if t['expected_result'] == 'fail' and not r.success)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()