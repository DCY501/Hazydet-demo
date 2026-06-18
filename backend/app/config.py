"""
Demo 后端配置

模型权重路径在这里配置。后续只要替换 weights/ 目录下的 .pt 文件即可，
不需要改代码。
"""
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 权重目录
WEIGHTS_DIR = BASE_DIR / "weights"

# 结果输出目录
RESULTS_DIR = BASE_DIR / "results"
RESULTS_IMAGES_DIR = RESULTS_DIR / "images"
RESULTS_VIDEOS_DIR = RESULTS_DIR / "videos"

# 确保目录存在
RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# 模型配置
# key: 模型标识（前端用）
# name: 显示名称
# path: 权重文件路径
# description: 模型简介
MODELS = {
    "baseline": {
        "name": "Baseline",
        "path": WEIGHTS_DIR / "baseline.pt",
        "description": "原始 YOLOv8n，无去雾增强",
        "has_intermediate": False,
    },
    "phase1": {
        "name": "方案一",
        "path": WEIGHTS_DIR / "phase1.pt",
        "description": "AOD-Net 前置去雾 + YOLOv8 检测",
        "has_intermediate": True,
        "intermediate_types": ["dehazed"],
    },
    "phase2": {
        "name": "方案二",
        "path": WEIGHTS_DIR / "phase2.pt",
        "description": "AFFM + RSM 多任务检测框架",
        "has_intermediate": True,
        # phase2 中间结果字段后续可能调整，这里先预留
        "intermediate_types": ["clear", "transmission", "atmosphere", "reconstruction"],
    },
}

# 允许上传的图片格式
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# 允许上传的视频格式
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

# 图片最大上传大小（MB）
MAX_IMAGE_SIZE_MB = 20

# 视频最大上传大小（MB）
MAX_VIDEO_SIZE_MB = 200
