"""
加雾合成 API
"""
from fastapi import APIRouter, File, Form, UploadFile

from app.services.image_service import synthesize_haze
from app.utils.image_utils import save_upload_file, validate_image

router = APIRouter(prefix="/haze", tags=["加雾合成"])


@router.post("/synthesize")
async def synthesize(
    image: UploadFile = File(..., description="上传的清晰图片"),
    beta: float = Form(1.0, description="雾浓度 beta"),
):
    """给清晰图片加雾，合成有雾图像。"""
    validate_image(image)

    input_path = save_upload_file(image)
    result = synthesize_haze(input_path, beta)

    return {
        "success": True,
        **result,
    }
