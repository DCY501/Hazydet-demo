"""
三模型对比 API
"""
from fastapi import APIRouter, File, Form, UploadFile

from app.services.image_service import compare_models
from app.services.model_manager import model_manager
from app.utils.image_utils import add_haze, read_image_rgb, save_image_rgb, save_upload_file, validate_image

router = APIRouter(prefix="/compare", tags=["三模型对比"])


@router.post("")
async def compare(
    file: UploadFile = File(..., description="上传的图片"),
    beta: float = Form(None, description="可选：雾浓度 beta，不传则不加雾"),
):
    """用所有可用模型对同一张图片进行检测对比，可选先加雾。"""
    validate_image(file)

    available = model_manager.model_names()
    if not available:
        return {
            "success": False,
            "error": "当前没有可用的模型，请检查 weights/ 目录下的权重文件",
            "available_models": model_manager.available_models(),
        }

    input_path = save_upload_file(file)

    # 如果指定了 beta，先对图片加雾
    if beta is not None and beta > 0:
        image = read_image_rgb(input_path)
        hazy_bgr = add_haze(image, beta=beta)
        hazy_rgb = hazy_bgr[..., ::-1]
        save_image_rgb(hazy_rgb, input_path)

    results = compare_models(input_path)

    return {
        "success": True,
        "results": results,
    }
