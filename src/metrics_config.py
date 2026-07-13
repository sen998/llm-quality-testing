"""
指标配置中心
统一管理 DeepEval 评测指标的配置
"""
from deepeval.metrics import (
    FaithfulnessMetric,
    HallucinationMetric,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    BiasMetric,
    ToxicityMetric
)


class MetricsConfig:
    """评测指标配置类"""

    # 默认评测模型（SiliconFlow）
    DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"

    # 备用模型（当主模型不可用时）
    BACKUP_MODEL = "Qwen/Qwen2.5-72B-Instruct"

    # 阈值配置
    THRESHOLDS = {
        "faithfulness": 0.7,
        "hallucination": 0.5,
        "answer_relevancy": 0.7,
        "contextual_relevancy": 0.6,
        "bias": 0.5,
        "toxicity": 0.5
    }

    @classmethod
    def get_faithfulness_metric(cls, model: str = None, threshold: float = None):
        """获取忠实度指标"""
        return FaithfulnessMetric(
            threshold=threshold or cls.THRESHOLDS["faithfulness"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_hallucination_metric(cls, model: str = None, threshold: float = None):
        """获取幻觉检测指标"""
        return HallucinationMetric(
            threshold=threshold or cls.THRESHOLDS["hallucination"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_answer_relevancy_metric(cls, model: str = None, threshold: float = None):
        """获取答案相关性指标"""
        return AnswerRelevancyMetric(
            threshold=threshold or cls.THRESHOLDS["answer_relevancy"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_contextual_relevancy_metric(cls, model: str = None, threshold: float = None):
        """获取上下文相关性指标"""
        return ContextualRelevancyMetric(
            threshold=threshold or cls.THRESHOLDS["contextual_relevancy"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_bias_metric(cls, model: str = None, threshold: float = None):
        """获取偏见检测指标"""
        return BiasMetric(
            threshold=threshold or cls.THRESHOLDS["bias"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_toxicity_metric(cls, model: str = None, threshold: float = None):
        """获取毒性检测指标"""
        return ToxicityMetric(
            threshold=threshold or cls.THRESHOLDS["toxicity"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_all_metrics(cls, model: str = None):
        """获取所有指标（用于综合评测）"""
        return [
            cls.get_faithfulness_metric(model),
            cls.get_answer_relevancy_metric(model),
            cls.get_hallucination_metric(model)
        ]


# 便捷函数
def get_metric(metric_name: str, **kwargs):
    """通过名称获取指标"""
    metric_map = {
        "faithfulness": MetricsConfig.get_faithfulness_metric,
        "hallucination": MetricsConfig.get_hallucination_metric,
        "answer_relevancy": MetricsConfig.get_answer_relevancy_metric,
        "contextual_relevancy": MetricsConfig.get_contextual_relevancy_metric,
        "bias": MetricsConfig.get_bias_metric,
        "toxicity": MetricsConfig.get_toxicity_metric
    }

    if metric_name not in metric_map:
        raise ValueError(f"未知指标: {metric_name}，可用: {list(metric_map.keys())}")

    return metric_map[metric_name](**kwargs)