"""
Phase 1：AOD-Net 前置去雾 + YOLOv8 检测

当前为占位实现，直接复用标准 YOLO 推理。
后续替换为真实结构：
    1. 用 AOD-Net 对输入图像去雾得到清晰图 Ĵ
    2. 将 Ĵ 送入 YOLOv8 检测
    3. 中间结果返回去雾增强图
"""
from pathlib import Path
from typing import Any, Union

import numpy as np

from app.models.yolo_wrapper import YOLOWrapper


class Phase1Model(YOLOWrapper):
    """
    Phase 1 占位模型。

    目前结构与 YOLO 一致，仅作为接口占位。
    后续实现 AOD-Net 去雾模块后，重写 predict / predict_array / intermediate 方法即可。
    """

    def __init__(self, weight_path: Union[str, Path]):
        super().__init__(weight_path)
        print("[Phase1Model] 当前为占位实现，后续接入 AOD-Net 去雾模块")

    def predict(self, image_path: Union[str, Path]) -> Any:
        # TODO: 接入 AOD-Net 去雾后再调用 YOLO 检测
        return super().predict(image_path)

    def predict_array(self, image: np.ndarray) -> Any:
        # TODO: 接入 AOD-Net 去雾后再调用 YOLO 检测
        return super().predict_array(image)

    def intermediate(self, image_path: Union[str, Path]) -> dict:
        """
        返回中间结果。

        Phase 1 应返回：
            - dehazed: 去雾增强图 URL 或路径
        """
        # TODO: 生成真实的去雾增强图
        return {
            "dehazed": None,
            "note": "Phase1 占位：AOD-Net 去雾模块待实现",
        }

    def info(self) -> dict:
        info = super().info()
        info["description"] = "AOD-Net 前置去雾 + YOLOv8 检测（占位）"
        return info
