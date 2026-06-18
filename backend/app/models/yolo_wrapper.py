"""
标准 YOLO 模型的包装类

用于 baseline 或任何直接基于 Ultralytics YOLO 训练得到的权重。
"""
from pathlib import Path
from typing import Any, Union

import numpy as np
from ultralytics import YOLO

from app.models.base_model import HazyDetModel


class YOLOWrapper(HazyDetModel):
    """
    标准 YOLO 包装器。

    加载 .pt 权重后，提供统一的 predict / predict_array / intermediate 接口。
    """

    def __init__(self, weight_path: Union[str, Path]):
        self.weight_path = Path(weight_path)
        self.model = YOLO(str(self.weight_path))
        print(f"[YOLOWrapper] 已加载权重: {self.weight_path}")

    def predict(self, image_path: Union[str, Path]) -> Any:
        results = self.model(str(image_path))
        return results[0]

    def predict_array(self, image: np.ndarray) -> Any:
        results = self.model(image)
        return results[0]

    def info(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "weight_path": str(self.weight_path),
            "task": getattr(self.model, "task", "unknown"),
        }
