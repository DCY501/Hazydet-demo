"""
视频检测 API（后续实现）
"""
from fastapi import APIRouter, File, Form, UploadFile

from app.services.model_manager import model_manager
from app.utils.image_utils import save_upload_file, validate_video

router = APIRouter(prefix="/video", tags=["视频检测"])


@router.post("")
async def detect_video(
    file: UploadFile = File(..., description="上传的视频"),
    model: str = Form("baseline", description="模型名称"),
):
    """视频检测接口，后续实现。"""
    validate_video(file)

    if not model_manager.is_available(model):
        return {
            "success": False,
            "error": f"模型 '{model}' 当前不可用",
            "available_models": model_manager.available_models(),
        }

    # 仅保存上传文件，后续补充逐帧检测逻辑
    input_path = save_upload_file(file)

    return {
        "success": False,
        "message": "视频检测功能开发中",
        "input_path": str(input_path),
        "model": model,
    }
