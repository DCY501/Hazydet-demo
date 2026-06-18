"""
三模型对比 API
"""
from fastapi import APIRouter, File, UploadFile

from app.services.image_service import compare_models
from app.services.model_manager import model_manager
from app.utils.image_utils import save_upload_file, validate_image

router = APIRouter(prefix="/compare", tags=["三模型对比"])


@router.post("")
async def compare(image: UploadFile = File(..., description="上传的图片")):
    """用所有可用模型对同一张图片进行检测对比。"""
    validate_image(image)

    available = model_manager.model_names()
    if not available:
        return {
            "success": False,
            "error": "当前没有可用的模型，请检查 weights/ 目录下的权重文件",
            "available_models": model_manager.available_models(),
        }

    input_path = save_upload_file(image)
    results = compare_models(input_path)

    return {
        "success": True,
        "results": results,
    }
