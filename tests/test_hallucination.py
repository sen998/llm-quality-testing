"""
幻觉检测（Hallucination）
验证 LLM 回答是否包含虚构或错误信息
"""
import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase


@pytest.mark.slow
@pytest.mark.xfail(reason="故意测试幻觉检测，预期检测到幻觉")
def test_hallucination_detected(eval_model):
    """测试：检测到明显的事实错误（幻觉）"""
    context = ["Python 由 Guido van Rossum 于1991年创建。"]

    test_case = LLMTestCase(
        input="Python 是谁创建的？",
        actual_output="Python 是由 James Gosling 在1995年创建的，主要用于企业级开发。",
        context=context
    )

    metric = HallucinationMetric(threshold=0.5, model=eval_model)
    assert_test(test_case, [metric])


@pytest.mark.slow
def test_no_hallucination(eval_model):
    """测试：正确回答，无幻觉 — 预期通过"""
    context = ["Python 由 Guido van Rossum 于1991年创建。"]

    test_case = LLMTestCase(
        input="Python 是谁创建的？",
        actual_output="Python 是由 Guido van Rossum 在1991年创建的。",
        context=context
    )

    metric = HallucinationMetric(threshold=0.5, model=eval_model)
    assert_test(test_case, [metric])
