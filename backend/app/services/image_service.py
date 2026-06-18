"""
图片检测相关业务逻辑
"""
from pathlib import Path

import cv2
import numpy as np

from app.config import MODELS, RESULTS_IMAGES_DIR
from app.services.model_manager import model_manager
from app.utils.image_utils import (
    add_haze,
    compute_metrics,
    generate_result_filename,
    parse_detection_results,
    read_image_rgb,
    save_image_rgb,
)


def detect_image(input_path: Path, model_key: str) -> dict:
    """
    对单张图片进行检测。

    Args:
        input_path: 输入图片路径
        model_key: 模型标识

    Returns:
        包含结果图 URL、检测框、指标的字典
    """
    if not model_manager.is_available(model_key):
        raise ValueError(f"模型不可用: {model_key}")

    model = model_manager.get(model_key)
    results = model(str(input_path))
    result = results[0]

    # 保存结果图
    result_filename = generate_result_filename(prefix=model_key)
    result_path = RESULTS_IMAGES_DIR / result_filename
    result.save(str(result_path))

    # 解析结果
    detections, class_distribution = parse_detection_results(result)
    metrics = compute_metrics(detections)

    # 提取推理耗时（YOLO speed 字典包含 preprocess/inference/postprocess，单位 ms）
    inference_ms = 0.0
    if hasattr(result, "speed") and isinstance(result.speed, dict):
        inference_ms = round(result.speed.get("inference", 0.0), 2)

    return {
        "result_url": f"/results/images/{result_filename}",
        "metrics": {
            "count": metrics["count"],
            "avg_conf": metrics["avg_conf"],
            "inference_ms": inference_ms,
        },
        "detections": detections,
        "class_distribution": class_distribution,
    }


def compare_models(input_path: Path) -> dict:
    """
    用所有可用模型对同一张图片进行检测，返回对比结果。
    """
    available = model_manager.model_names()
    if not available:
        raise ValueError("当前没有可用的模型")

    results = {}
    for model_key in available:
        try:
            results[model_key] = detect_image(input_path, model_key)
            results[model_key]["name"] = MODELS[model_key]["name"]
            results[model_key]["description"] = MODELS[model_key]["description"]
        except Exception as e:
            results[model_key] = {
                "name": MODELS[model_key]["name"],
                "error": str(e),
            }

    return results


def synthesize_haze(input_path: Path, beta: float) -> dict:
    """
    给图片加雾。

    Args:
        input_path: 输入图片路径
        beta: 雾浓度

    Returns:
        有雾图片 URL
    """
    image = read_image_rgb(input_path)
    hazy_bgr = add_haze(image, beta=beta)

    result_filename = generate_result_filename(prefix=f"haze_beta{beta:.2f}")
    result_path = RESULTS_IMAGES_DIR / result_filename
    hazy_rgb = cv2.cvtColor(hazy_bgr, cv2.COLOR_BGR2RGB)
    save_image_rgb(hazy_rgb, result_path)

    return {
        "haze_url": f"/results/images/{result_filename}",
        "beta": beta,
    }


def get_intermediate_results(input_path: Path, model_key: str) -> dict:
    """
    获取模型的中间结果。

    不同模型返回不同的中间结果，字段可扩展。
    目前：
    - phase1: dehazed
    - phase2: clear, transmission, atmosphere, reconstruction（占位，后续实现）
    - baseline: 无
    """
    if not model_manager.is_available(model_key):
        raise ValueError(f"模型不可用: {model_key}")

    cfg = MODELS.get(model_key, {})
    if not cfg.get("has_intermediate", False):
        return {"intermediate": {}}

    # TODO: 根据模型实际结构提取中间结果
    # 目前先返回占位符，后续根据 phase1/phase2 的具体实现补充

    intermediate_types = cfg.get("intermediate_types", [])
    intermediate = {}

    for itype in intermediate_types:
        placeholder_filename = generate_result_filename(prefix=f"{model_key}_{itype}")
        intermediate[itype] = f"/results/images/{placeholder_filename}"

    return {"intermediate": intermediate}
