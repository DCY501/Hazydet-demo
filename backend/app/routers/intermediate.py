"""
中间结果可视化 API
"""
from fastapi import APIRouter, File, Form, UploadFile

from app.services.image_service import detect_image, get_intermediate_results
from app.services.model_manager import model_manager
from app.utils.image_utils import save_upload_file, validate_image

router = APIRouter(prefix="/intermediate", tags=["中间结果"])


@router.post("")
async def intermediate(
    file: UploadFile = File(..., description="上传的图片"),
    model: str = Form("phase2", description="模型名称：baseline / phase1 / phase2"),
):
    """
    获取模型中间结果。

    - baseline: 无中间结果
    - phase1: 返回去雾增强图
    - phase2: 返回 jhat/transmission/atmosphere/reconstruction 等（后续实现）
    """
    validate_image(file)

    if not model_manager.is_available(model):
        return {
            "success": False,
            "error": f"模型 '{model}' 当前不可用",
            "available_models": model_manager.available_models(),
        }

    input_path = save_upload_file(file)

    # 先跑检测，得到结果图
    detect_result = detect_image(input_path, model)

    # 再取中间结果（目前为占位，后续补充实际提取逻辑）
    intermediate_result = get_intermediate_results(input_path, model)

    return {
        "success": True,
        "model": model,
        "result_url": detect_result["result_url"],
        "metrics": detect_result["metrics"],
        **intermediate_result,
    }
