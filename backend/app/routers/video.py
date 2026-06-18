"""
视频检测 API（后续实现）
"""
from fastapi import APIRouter

router = APIRouter(prefix="/video", tags=["视频检测"])


@router.post("/detect")
async def detect_video():
    """视频检测接口，后续实现。"""
    return {
        "success": False,
        "message": "视频检测功能开发中",
    }
