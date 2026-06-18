"""
单图检测 API
"""
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile

from app.services.image_service import detect_image
from app.services.model_manager import model_manager
from app.utils.image_utils import add_haze, read_image_rgb, save_image_rgb, save_upload_file, validate_image

router = APIRouter(prefix="/detect", tags=["单图检测"])


@router.post("")
async def detect(
    file: UploadFile = File(..., description="上传的图片"),
    model: str = Form("baseline", description="模型名称：baseline / phase1 / phase2"),
    beta: float = Form(None, description="可选：雾浓度 beta，不传则不加雾"),
):
    """对单张图片进行目标检测，可选先加雾。"""
    validate_image(file)

    if not model_manager.is_available(model):
        return {
            "success": False,
            "error": f"模型 '{model}' 当前不可用，请检查 weights/ 目录下是否存在对应权重文件",
            "available_models": model_manager.available_models(),
        }

    input_path = save_upload_file(file)

    # 如果指定了 beta，先对图片加雾
    if beta is not None and beta > 0:
        image = read_image_rgb(input_path)
        hazy_bgr = add_haze(image, beta=beta)
        hazy_rgb = hazy_bgr[..., ::-1]  # BGR -> RGB
        save_image_rgb(hazy_rgb, input_path)

    result = detect_image(input_path, model)

    return {
        "success": True,
        "model": model,
        **result,
    }


@router.get("/models")
async def list_models():
    """获取当前可用的模型列表。"""
    return {
        "success": True,
        "models": model_manager.available_models(),
    }
