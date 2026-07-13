"""
测试数据生成器
利用爬虫技术自动生成评测数据集
"""
import json
import random
from typing import List, Dict
import requests
from datetime import datetime


class TestDataGenerator:
    """测试数据生成器"""

    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        self.knowledge_base = []

    def load_knowledge_base(self, filepath: str) -> List[Dict]:
        """从 JSON 加载知识库"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.knowledge_base = data.get("contexts", [])
        return self.knowledge_base

    def generate_qa_pairs(self, context: Dict, num_pairs: int = 3) -> List[Dict]:
        """
        基于上下文生成问答对
        实际项目中可以接入 LLM API 自动生成
        """
        qa_pairs = []
        content = " ".join(context.get("content", []))

        # 简单规则生成（实际中可用 LLM 生成更复杂的）
        topic = context.get("topic", "未知主题")

        # 正面用例：正确回答
        qa_pairs.append({
            "id": f"{context['id']}-Q{len(qa_pairs) + 1}",
            "category": "faithfulness",
            "type": "positive",
            "input": f"{topic} 的关键信息是什么？",
            "actual_output": content[:100] + "...",
            "context_id": context["id"],
            "expected_result": "pass",
            "description": "基于上下文的正确回答"
        })

        # 负面用例：幻觉
        qa_pairs.append({
            "id": f"{context['id']}-Q{len(qa_pairs) + 1}",
            "category": "hallucination",
            "type": "negative",
            "input": f"{topic} 是谁创建的？",
            "actual_output": f"这是关于 {topic} 的虚构信息，用于测试幻觉检测。",
            "context_id": context["id"],
            "expected_result": "fail",
            "description": "包含幻觉的错误回答"
        })

        return qa_pairs

    def generate_from_knowledge_base(self) -> List[Dict]:
        """从知识库批量生成测试用例"""
        all_test_cases = []

        for context in self.knowledge_base:
            cases = self.generate_qa_pairs(context)
            all_test_cases.extend(cases)

        return all_test_cases

    def save_test_cases(self, test_cases: List[Dict], filename: str = "generated_tests.json"):
        """保存生成的测试用例到文件"""
        output_path = f"{self.output_dir}/{filename}"

        data = {
            "description": "自动生成的测试用例",
            "generated_at": datetime.now().isoformat(),
            "total_cases": len(test_cases),
            "test_cases": test_cases
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ 已保存 {len(test_cases)} 个测试用例到 {output_path}")
        return output_path

    def fetch_web_content(self, url: str) -> str:
        """
        爬取网页内容（利用你的爬虫技术）
        实际项目中可接入真实数据源
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ 爬取失败: {url}, 错误: {e}")
            return ""

    def generate_from_web(self, url: str, topic: str) -> List[Dict]:
        """
        从网页内容生成测试用例
        展示爬虫 + AI 测试的结合
        """
        print(f"🕷️ 正在爬取: {url}")
        content = self.fetch_web_content(url)

        if not content:
            return []

        # 简化处理：提取前 500 字符作为上下文
        context_text = content[:500]

        test_cases = [
            {
                "id": f"web-{random.randint(1000, 9999)}",
                "category": "faithfulness",
                "type": "positive",
                "input": f"关于 {topic} 的主要信息是什么？",
                "actual_output": context_text[:100],
                "context": [context_text],
                "expected_result": "pass",
                "description": f"从网页 {url} 提取的测试数据"
            }
        ]

        return test_cases


def demo_generate():
    """演示：生成测试数据"""
    generator = TestDataGenerator()

    # 从已有知识库生成
    print("=" * 50)
    print("📝 从知识库生成测试用例")
    print("=" * 50)

    generator.load_knowledge_base("data/sample_contexts.json")
    test_cases = generator.generate_from_knowledge_base()

    # 保存
    generator.save_test_cases(test_cases, "generated_from_kb.json")

    # 统计
    categories = {}
    for case in test_cases:
        cat = case["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\n📊 生成统计:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} 个")


if __name__ == "__main__":
    demo_generate()