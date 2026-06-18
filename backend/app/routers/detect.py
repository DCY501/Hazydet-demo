"""
单图检测 API
"""
from fastapi import APIRouter, File, Form, UploadFile

from app.services.image_service import detect_image
from app.services.model_manager import model_manager
from app.utils.image_utils import save_upload_file, validate_image

router = APIRouter(prefix="/detect", tags=["单图检测"])


@router.post("")
async def detect(
    image: UploadFile = File(..., description="上传的图片"),
    model: str = Form("phase2", description="模型名称：baseline / phase1 / phase2"),
):
    """对单张图片进行目标检测。"""
    validate_image(image)

    if not model_manager.is_available(model):
        return {
            "success": False,
            "error": f"模型 '{model}' 当前不可用，请检查 weights/ 目录下是否存在对应权重文件",
            "available_models": model_manager.available_models(),
        }

    input_path = save_upload_file(image)
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
