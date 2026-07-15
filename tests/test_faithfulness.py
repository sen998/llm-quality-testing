"""
忠实度测试（Faithfulness）
验证 LLM 回答是否忠实于检索到的上下文
"""
import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase


@pytest.mark.slow
def test_faithfulness_pass(eval_model, sample_context):
    """测试1：回答忠实于上下文 — 预期通过"""
    test_case = LLMTestCase(
        input="Python 是谁创建的？什么时候创建的？",
        actual_output="Python 是由 Guido van Rossum 在1991年创建的，是一种强调代码可读性的高级编程语言。",
        retrieval_context=sample_context
    )

    metric = FaithfulnessMetric(threshold=0.7, model=eval_model)
    assert_test(test_case, [metric])


@pytest.mark.slow
def test_faithfulness_fail(eval_model, sample_context):
    """测试2：回答包含上下文外的信息 — 预期检测到不忠实"""
    test_case = LLMTestCase(
        input="Python 是谁创建的？",
        actual_output="Python 是由 Guido van Rossum 在1991年创建的，同时 Java 也是由 James Gosling 在1995年创建的。",
        retrieval_context=sample_context
    )

    metric = FaithfulnessMetric(threshold=0.7, model=eval_model)
    assert_test(test_case, [metric])
