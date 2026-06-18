"""
模型结构包

提供统一的 HazyDetModel 接口，以及各方案模型的占位/实现类。
"""
from app.models.base_model import HazyDetModel
from app.models.yolo_wrapper import YOLOWrapper
from app.models.phase1_model import Phase1Model
from app.models.phase2_model import Phase2Model
from app.models.model_factory import create_model

__all__ = [
    "HazyDetModel",
    "YoloWrapper",
    "Phase1Model",
    "Phase2Model",
    "create_model",
]
