"""
相关性测试（Answer Relevancy）
验证 LLM 回答是否切题
"""
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase


@pytest.mark.slow
def test_relevancy_pass(eval_model):
    """测试：回答切题 — 预期通过"""
    test_case = LLMTestCase(
        input="Python 的创建者是谁？",
        actual_output="Python 的创建者是 Guido van Rossum，他在1991年创建了这门语言。"
    )

    metric = AnswerRelevancyMetric(threshold=0.7, model=eval_model)
    assert_test(test_case, [metric])


@pytest.mark.slow
@pytest.mark.xfail(reason="故意测试答非所问，预期检测到不相关")
def test_relevancy_fail(eval_model):
    """测试：答非所问 — 预期检测到不相关"""
    test_case = LLMTestCase(
        input="Python 的创建者是谁？",
        actual_output="Python 是一种非常流行的编程语言，它的语法简洁优雅，适合初学者学习。"
    )

    metric = AnswerRelevancyMetric(threshold=0.7, model=eval_model)
    assert_test(test_case, [metric])