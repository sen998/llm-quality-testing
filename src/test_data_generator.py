"""
娴嬭瘯鏁版嵁鐢熸垚鍣?
鍒╃敤鐖櫕鎶€鏈嚜鍔ㄧ敓鎴愯瘎娴嬫暟鎹泦
"""
import json
import random
from typing import List, Dict
import requests
from datetime import datetime


class TestDataGenerator:
    """娴嬭瘯鏁版嵁鐢熸垚鍣?""

    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        self.knowledge_base = []

    def load_knowledge_base(self, filepath: str) -> List[Dict]:
        """浠?JSON 鍔犺浇鐭ヨ瘑搴?""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.knowledge_base = data.get("contexts", [])
        return self.knowledge_base

    def generate_qa_pairs(self, context: Dict, num_pairs: int = 3) -> List[Dict]:
        """
        鍩轰簬涓婁笅鏂囩敓鎴愰棶绛斿
        瀹為檯椤圭洰涓彲浠ユ帴鍏?LLM API 鑷姩鐢熸垚
        """
        qa_pairs = []
        content = " ".join(context.get("content", []))

        # 绠€鍗曡鍒欑敓鎴愶紙瀹為檯涓彲鐢?LLM 鐢熸垚鏇村鏉傜殑锛?
        topic = context.get("topic", "鏈煡涓婚")

        # 姝ｉ潰鐢ㄤ緥锛氭纭洖绛?
        qa_pairs.append({
            "id": f"{context['id']}-Q{len(qa_pairs) + 1}",
            "category": "faithfulness",
            "type": "positive",
            "input": f"{topic} 鐨勫叧閿俊鎭槸浠€涔堬紵",
            "actual_output": content[:100] + "...",
            "context_id": context["id"],
            "expected_result": "pass",
            "description": "鍩轰簬涓婁笅鏂囩殑姝ｇ‘鍥炵瓟"
        })

        # 璐熼潰鐢ㄤ緥锛氬够瑙?
        qa_pairs.append({
            "id": f"{context['id']}-Q{len(qa_pairs) + 1}",
            "category": "hallucination",
            "type": "negative",
            "input": f"{topic} 鏄皝鍒涘缓鐨勶紵",
            "actual_output": f"杩欐槸鍏充簬 {topic} 鐨勮櫄鏋勪俊鎭紝鐢ㄤ簬娴嬭瘯骞昏妫€娴嬨€?,
            "context_id": context["id"],
            "expected_result": "fail",
            "description": "鍖呭惈骞昏鐨勯敊璇洖绛?
        })

        return qa_pairs

    def generate_from_knowledge_base(self) -> List[Dict]:
        """浠庣煡璇嗗簱鎵归噺鐢熸垚娴嬭瘯鐢ㄤ緥"""
        all_test_cases = []

        for context in self.knowledge_base:
            cases = self.generate_qa_pairs(context)
            all_test_cases.extend(cases)

        return all_test_cases

    def save_test_cases(self, test_cases: List[Dict], filename: str = "generated_tests.json"):
        """淇濆瓨鐢熸垚鐨勬祴璇曠敤渚嬪埌鏂囦欢"""
        output_path = f"{self.output_dir}/{filename}"

        data = {
            "description": "鑷姩鐢熸垚鐨勬祴璇曠敤渚?,
            "generated_at": datetime.now().isoformat(),
            "total_cases": len(test_cases),
            "test_cases": test_cases
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"鉁?宸蹭繚瀛?{len(test_cases)} 涓祴璇曠敤渚嬪埌 {output_path}")
        return output_path

    def fetch_web_content(self, url: str) -> str:
        """
        鐖彇缃戦〉鍐呭锛堝埄鐢ㄤ綘鐨勭埇铏妧鏈級
        瀹為檯椤圭洰涓彲鎺ュ叆鐪熷疄鏁版嵁婧?
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"鉂?鐖彇澶辫触: {url}, 閿欒: {e}")
            return ""

    def generate_from_web(self, url: str, topic: str) -> List[Dict]:
        """
        浠庣綉椤靛唴瀹圭敓鎴愭祴璇曠敤渚?
        灞曠ず鐖櫕 + AI 娴嬭瘯鐨勭粨鍚?
        """
        print(f"馃暦锔?姝ｅ湪鐖彇: {url}")
        content = self.fetch_web_content(url)

        if not content:
            return []

        # 绠€鍖栧鐞嗭細鎻愬彇鍓?500 瀛楃浣滀负涓婁笅鏂?
        context_text = content[:500]

        test_cases = [
            {
                "id": f"web-{random.randint(1000, 9999)}",
                "category": "faithfulness",
                "type": "positive",
                "input": f"鍏充簬 {topic} 鐨勪富瑕佷俊鎭槸浠€涔堬紵",
                "actual_output": context_text[:100],
                "context": [context_text],
                "expected_result": "pass",
                "description": f"浠庣綉椤?{url} 鎻愬彇鐨勬祴璇曟暟鎹?
            }
        ]

        return test_cases


def demo_generate():
    """婕旂ず锛氱敓鎴愭祴璇曟暟鎹?""
    generator = TestDataGenerator()

    # 浠庡凡鏈夌煡璇嗗簱鐢熸垚
    print("=" * 50)
    print("馃摑 浠庣煡璇嗗簱鐢熸垚娴嬭瘯鐢ㄤ緥")
    print("=" * 50)

    generator.load_knowledge_base("data/sample_contexts.json")
    test_cases = generator.generate_from_knowledge_base()

    # 淇濆瓨
    generator.save_test_cases(test_cases, "generated_from_kb.json")

    # 缁熻
    categories = {}
    for case in test_cases:
        cat = case["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\n馃搳 鐢熸垚缁熻:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} 涓?)


if __name__ == "__main__":
    demo_generate()
