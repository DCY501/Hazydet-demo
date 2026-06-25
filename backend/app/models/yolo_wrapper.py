"""
标准 YOLO 模型的包装类

用于 baseline 或任何直接基于 Ultralytics YOLO 训练得到的权重。
"""
from pathlib import Path
from typing import Any, List, Union

import numpy as np
from ultralytics import YOLO

from app.models.base_model import HazyDetModel


class YOLOWrapper(HazyDetModel):
    """
    标准 YOLO 包装器。

    加载 .pt 权重后，提供统一的 predict / predict_array / predict_batch / intermediate 接口。
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

    def predict_batch(self, images: List[np.ndarray]) -> List[Any]:
        """
        对一批图像进行批量推理。

        Args:
            images: BGR 格式的 OpenCV 图像列表

        Returns:
            检测结果列表，与输入顺序一致
        """
        if not images:
            return []

        # Ultralytics 支持 list of ndarray 作为 batch 输入
        results = self.model(images)
        return list(results)

    def info(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "weight_path": str(self.weight_path),
            "task": getattr(self.model, "task", "unknown"),
        }
