"""
图像处理工具函数
"""
import math
import uuid
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from fastapi import HTTPException, UploadFile

from app.config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    MAX_IMAGE_SIZE_MB,
    MAX_VIDEO_SIZE_MB,
    RESULTS_IMAGES_DIR,
    RESULTS_VIDEOS_DIR,
)


def validate_image(file: UploadFile) -> None:
    """验证上传的图片是否合法。"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名为空")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的图片格式: {ext}，请上传 {ALLOWED_IMAGE_EXTENSIONS}"
        )


def validate_video(file: UploadFile) -> None:
    """验证上传的视频是否合法。"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名为空")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的视频格式: {ext}，请上传 {ALLOWED_VIDEO_EXTENSIONS}"
        )


def save_upload_file(file: UploadFile, suffix: str = ".jpg") -> Path:
    """保存上传的文件到结果目录，返回保存路径。"""
    filename = f"upload_{uuid.uuid4().hex}{suffix}"
    save_path = RESULTS_IMAGES_DIR / filename
    contents = file.file.read()

    # 检查大小
    size_mb = len(contents) / (1024 * 1024)
    if suffix in ALLOWED_IMAGE_EXTENSIONS and size_mb > MAX_IMAGE_SIZE_MB:
        raise HTTPException(status_code=413, detail=f"图片过大，超过 {MAX_IMAGE_SIZE_MB}MB")
    if suffix in ALLOWED_VIDEO_EXTENSIONS and size_mb > MAX_VIDEO_SIZE_MB:
        raise HTTPException(status_code=413, detail=f"视频过大，超过 {MAX_VIDEO_SIZE_MB}MB")

    save_path.write_bytes(contents)
    return save_path


def generate_result_filename(prefix: str = "result", suffix: str = ".jpg") -> str:
    """生成结果文件名。"""
    return f"{prefix}_{uuid.uuid4().hex}{suffix}"


def read_image_rgb(path: Path) -> np.ndarray:
    """读取图片并转为 RGB 格式。"""
    img = cv2.imread(str(path))
    if img is None:
        raise HTTPException(status_code=400, detail="无法读取图片")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def save_image_rgb(image: np.ndarray, path: Path) -> None:
    """保存 RGB 图片。"""
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(path), bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])


def add_haze(image: np.ndarray, beta: float = 1.35, atmosphere: float = 0.82) -> np.ndarray:
    """
    给图片加雾。使用大气散射模型。

    Args:
        image: 输入图片，BGR 格式，uint8
        beta: 雾浓度
        atmosphere: 大气光强度

    Returns:
        有雾图片，BGR 格式，uint8
    """
    h, w = image.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    center_x, center_y = w * 0.5, h * 0.58
    distance = np.sqrt((xx - center_x) ** 2 + (yy - center_y) ** 2)
    depth = distance / (math.sqrt(center_x**2 + center_y**2) + 1e-6)
    transmission = np.exp(-beta * depth).astype(np.float32)
    transmission = cv2.GaussianBlur(transmission, (0, 0), sigmaX=25, sigmaY=25)
    transmission = transmission[..., None]

    img = image.astype(np.float32) / 255.0
    hazy = img * transmission + atmosphere * (1.0 - transmission)
    return np.clip(hazy * 255.0, 0, 255).astype(np.uint8)


def parse_detection_results(result) -> Tuple[list, dict]:
    """
    解析 YOLO 检测结果。

    Returns:
        detections: 检测框列表
        class_distribution: 类别数量分布
    """
    detections = []
    class_distribution = {}

    names = result.names if hasattr(result, "names") else {}

    if not hasattr(result, "boxes") or result.boxes is None:
        return detections, class_distribution

    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        cls_name = names.get(cls_id, str(cls_id))

        detections.append({
            "class": cls_name,
            "confidence": round(conf, 3),
            "bbox": [round(x1), round(y1), round(x2), round(y2)],
        })

        class_distribution[cls_name] = class_distribution.get(cls_name, 0) + 1

    return detections, class_distribution


def compute_metrics(detections: list) -> dict:
    """计算检测指标。"""
    if not detections:
        return {"count": 0, "avg_confidence": 0.0}

    confidences = [d["confidence"] for d in detections]
    return {
        "count": len(detections),
        "avg_confidence": round(sum(confidences) / len(confidences), 3),
    }
