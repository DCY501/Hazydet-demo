"""
Phase 2：AFFM + RSM 多任务检测框架

当前为占位实现，直接复用标准 YOLO 推理。
后续替换为真实结构：
    1. 编码器提取多尺度特征
    2. AFFM（Adaptive Feature Fusion Module）融合去雾与检测特征
    3. RSM（Restoration Sub-network）输出 Ĵ / t / A / reconstruction
    4. 检测头在融合特征上预测目标
"""
from pathlib import Path
from typing import Any, Union

import numpy as np

from app.models.yolo_wrapper import YOLOWrapper


class Phase2Model(YOLOWrapper):
    """
    Phase 2 占位模型。

    目前结构与 YOLO 一致，仅作为接口占位。
    后续实现 AFFM + RSM 模块后，重写 predict / predict_array / intermediate 方法即可。
    """

    def __init__(self, weight_path: Union[str, Path]):
        super().__init__(weight_path)
        print("[Phase2Model] 当前为占位实现，后续接入 AFFM + RSM 多任务模块")

    def predict(self, image_path: Union[str, Path]) -> Any:
        # TODO: 接入 AFFM + RSM 后再调用检测头
        return super().predict(image_path)

    def predict_array(self, image: np.ndarray) -> Any:
        # TODO: 接入 AFFM + RSM 后再调用检测头
        return super().predict_array(image)

    def intermediate(self, image_path: Union[str, Path]) -> dict:
        """
        返回中间结果。

        Phase 2 应返回：
            - jhat: 清晰图像估计 Ĵ
            - transmission: 透射率图 t
            - atmosphere: 大气光 A
            - reconstruction: 重构图
        """
        # TODO: 从模型中提取真实中间特征图
        return {
            "jhat": None,
            "transmission": None,
            "atmosphere": None,
            "reconstruction": None,
            "note": "Phase2 占位：AFFM + RSM 中间结果提取待实现",
        }

    def info(self) -> dict:
        info = super().info()
        info["description"] = "AFFM + RSM 多任务检测框架（占位）"
        return info
