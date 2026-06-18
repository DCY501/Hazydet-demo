"""
模型工厂

根据配置中的 model_key 创建对应的模型实例。
新增模型方案时，只需在这里注册即可。
"""
from pathlib import Path
from typing import Union

from app.models.base_model import HazyDetModel
from app.models.phase1_model import Phase1Model
from app.models.phase2_model import Phase2Model
from app.models.yolo_wrapper import YOLOWrapper


# 模型 key -> 模型类的映射表
_MODEL_REGISTRY = {
    "baseline": YOLOWrapper,
    "phase1": Phase1Model,
    "phase2": Phase2Model,
}


def create_model(model_key: str, weight_path: Union[str, Path]) -> HazyDetModel:
    """
    根据 model_key 创建对应的模型实例。

    Args:
        model_key: 模型标识，如 baseline / phase1 / phase2
        weight_path: 权重文件路径

    Returns:
        HazyDetModel 实例

    Raises:
        ValueError: 如果 model_key 未注册
    """
    model_cls = _MODEL_REGISTRY.get(model_key)
    if model_cls is None:
        print(f"[ModelFactory] 未注册的模型 key: {model_key}， fallback 到标准 YOLO")
        model_cls = YOLOWrapper

    return model_cls(weight_path)


def register_model(model_key: str, model_cls: type[HazyDetModel]) -> None:
    """
    注册新的模型类型，方便后续动态扩展。

    Args:
        model_key: 模型标识
        model_cls: 继承自 HazyDetModel 的类
    """
    _MODEL_REGISTRY[model_key] = model_cls
    print(f"[ModelFactory] 已注册模型: {model_key} -> {model_cls.__name__}")


def list_registered_models() -> list[str]:
    """返回所有已注册的模型 key。"""
    return list(_MODEL_REGISTRY.keys())
