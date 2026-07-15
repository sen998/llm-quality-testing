"""
鎸囨爣閰嶇疆涓績
缁熶竴绠＄悊 DeepEval 璇勬祴鎸囨爣鐨勯厤缃?
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
    """璇勬祴鎸囨爣閰嶇疆绫?""

    # 榛樿璇勬祴妯″瀷锛圫iliconFlow锛?
    DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"

    # 澶囩敤妯″瀷锛堝綋涓绘ā鍨嬩笉鍙敤鏃讹級
    BACKUP_MODEL = "Qwen/Qwen2.5-72B-Instruct"

    # 闃堝€奸厤缃?
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
        """鑾峰彇蹇犲疄搴︽寚鏍?""
        return FaithfulnessMetric(
            threshold=threshold or cls.THRESHOLDS["faithfulness"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_hallucination_metric(cls, model: str = None, threshold: float = None):
        """鑾峰彇骞昏妫€娴嬫寚鏍?""
        return HallucinationMetric(
            threshold=threshold or cls.THRESHOLDS["hallucination"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_answer_relevancy_metric(cls, model: str = None, threshold: float = None):
        """鑾峰彇绛旀鐩稿叧鎬ф寚鏍?""
        return AnswerRelevancyMetric(
            threshold=threshold or cls.THRESHOLDS["answer_relevancy"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_contextual_relevancy_metric(cls, model: str = None, threshold: float = None):
        """鑾峰彇涓婁笅鏂囩浉鍏虫€ф寚鏍?""
        return ContextualRelevancyMetric(
            threshold=threshold or cls.THRESHOLDS["contextual_relevancy"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_bias_metric(cls, model: str = None, threshold: float = None):
        """鑾峰彇鍋忚妫€娴嬫寚鏍?""
        return BiasMetric(
            threshold=threshold or cls.THRESHOLDS["bias"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_toxicity_metric(cls, model: str = None, threshold: float = None):
        """鑾峰彇姣掓€ф娴嬫寚鏍?""
        return ToxicityMetric(
            threshold=threshold or cls.THRESHOLDS["toxicity"],
            model=model or cls.DEFAULT_MODEL,
            include_reason=True
        )

    @classmethod
    def get_all_metrics(cls, model: str = None):
        """鑾峰彇鎵€鏈夋寚鏍囷紙鐢ㄤ簬缁煎悎璇勬祴锛?""
        return [
            cls.get_faithfulness_metric(model),
            cls.get_answer_relevancy_metric(model),
            cls.get_hallucination_metric(model)
        ]


# 渚挎嵎鍑芥暟
def get_metric(metric_name: str, **kwargs):
    """閫氳繃鍚嶇О鑾峰彇鎸囨爣"""
    metric_map = {
        "faithfulness": MetricsConfig.get_faithfulness_metric,
        "hallucination": MetricsConfig.get_hallucination_metric,
        "answer_relevancy": MetricsConfig.get_answer_relevancy_metric,
        "contextual_relevancy": MetricsConfig.get_contextual_relevancy_metric,
        "bias": MetricsConfig.get_bias_metric,
        "toxicity": MetricsConfig.get_toxicity_metric
    }

    if metric_name not in metric_map:
        raise ValueError(f"鏈煡鎸囨爣: {metric_name}锛屽彲鐢? {list(metric_map.keys())}")

    return metric_map[metric_name](**kwargs)
