"""
统一模型接口基类

所有检测模型（baseline / phase1 / phase2）都需要实现这个接口，
这样上层业务代码（image_service / routers）不需要关心具体模型结构。
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union

import numpy as np


class HazyDetModel(ABC):
    """
    雾天目标检测模型统一接口。

    子类需要实现：
        - predict(image_path): 对图片文件路径推理
        - predict_array(image): 对 numpy 数组推理

    可选实现：
        - intermediate(image_path): 返回中间结果字典
    """

    @abstractmethod
    def predict(self, image_path: Union[str, Path]) -> Any:
        """
        对单张图片进行目标检测。

        Args:
            image_path: 图片文件路径

        Returns:
            检测结果对象，需包含 .boxes / .names 等 YOLO 风格属性，
            供 image_service.parse_detection_results 解析。
        """
        pass

    @abstractmethod
    def predict_array(self, image: np.ndarray) -> Any:
        """
        对 numpy 数组进行目标检测。

        Args:
            image: BGR 格式的 OpenCV 图像

        Returns:
            检测结果对象
        """
        pass

    def intermediate(self, image_path: Union[str, Path]) -> dict:
        """
        获取模型中间结果（如去雾图、透射率图等）。

        Args:
            image_path: 图片文件路径

        Returns:
            中间结果字典，键值由具体模型定义。
            例如 phase1 返回 {"dehazed": ...}，phase2 返回 {"jhat": ..., "transmission": ...}。
        """
        return {}

    def info(self) -> dict:
        """返回模型基本信息，用于日志或调试。"""
        return {"type": self.__class__.__name__}
