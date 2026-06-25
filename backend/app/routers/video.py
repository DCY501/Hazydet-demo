"""
视频检测 API（支持 SSE 实时进度推送）
"""
import asyncio
import json
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from app.services.model_manager import model_manager
from app.services.video_service import detect_video
from app.utils.image_utils import save_upload_file, validate_video

router = APIRouter(prefix="/video", tags=["视频检测"])


@router.post("")
async def detect_video_endpoint(
    file: UploadFile = File(..., description="上传的视频"),
    model: str = Form("baseline", description="模型名称"),
    detect_interval: int = Form(2, description="跳帧间隔，每隔多少帧检测一次"),
    batch_size: int = Form(4, description="GPU batch 大小"),
    use_batch: bool = Form(False, description="是否使用 GPU batch 推理加速"),
):
    """视频检测接口，逐帧处理并返回结果视频（支持跳帧和 GPU batch 加速）。"""
    validate_video(file)

    if not model_manager.is_available(model):
        return {
            "success": False,
            "error": f"模型 '{model}' 当前不可用",
            "available_models": model_manager.available_models(),
        }

    # 保存上传文件，保留原文件名（去除不安全字符）
    ext = Path(file.filename).suffix.lower() if file.filename else ".mp4"
    safe_stem = Path(file.filename).stem if file.filename else "video"
    # 移除可能导致路径问题的字符
    safe_stem = "".join(c for c in safe_stem if c.isalnum() or c in "-_ .").strip()
    input_filename = f"{safe_stem}{ext}"
    input_path = save_upload_file(file, suffix=ext, filename=input_filename)

    async def event_stream():
        loop = asyncio.get_event_loop()
        result_container = {}
        latest_progress = {"current": 0, "total": 0}

        def progress_callback(current: int, total: int):
            latest_progress["current"] = current
            latest_progress["total"] = total

        def run_detect():
            try:
                result = detect_video(
                    input_path,
                    model,
                    progress_callback=progress_callback,
                    detect_interval=detect_interval,
                    batch_size=batch_size,
                    use_batch=use_batch,
                )
                result_container["result"] = result
            except Exception as e:
                result_container["error"] = str(e)

        # 在后台线程运行同步的视频检测
        task = loop.run_in_executor(None, run_detect)

        # 轮询进度，直到任务完成
        while not task.done():
            await asyncio.sleep(0.5)
            current = latest_progress["current"]
            total = latest_progress["total"]
            percent = int(current / total * 100) if total > 0 else 0
            data = json.dumps({"type": "progress", "percent": percent, "current": current, "total": total})
            yield f"data: {data}\n\n".encode("utf-8")

        # 任务完成，获取结果
        await task
        if "error" in result_container:
            data = json.dumps({"type": "error", "error": result_container["error"]})
            yield f"data: {data}\n\n".encode("utf-8")
        else:
            data = json.dumps({"type": "complete", "result": result_container["result"]})
            yield f"data: {data}\n\n".encode("utf-8")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
