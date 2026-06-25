"""
视频检测业务逻辑
"""
import asyncio
import shutil
import time
from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np

from app.config import RESULTS_VIDEOS_DIR
from app.services.model_manager import model_manager
from app.utils.image_utils import draw_boxes_on_image, parse_detection_results


def _get_ffmpeg_exe() -> str | None:
    """获取 ffmpeg 可执行文件路径，优先使用 imageio-ffmpeg 自带的 ffmpeg。"""
    try:
        from imageio_ffmpeg import get_ffmpeg_exe
        return get_ffmpeg_exe()
    except Exception:
        pass
    return shutil.which("ffmpeg")


def detect_video(
    input_path: Path,
    model_key: str,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    detect_interval: int = 2,
    batch_size: int = 1,
    use_batch: bool = False,
) -> dict:
    """
    对视频进行逐帧目标检测（支持跳帧加速和 GPU batch 加速）。

    Args:
        input_path: 输入视频路径
        model_key: 模型标识
        progress_callback: 进度回调函数，接收 (current_frame, total_frames) 参数
        detect_interval: 每隔多少帧做一次模型推理，中间帧复用上一次检测结果
        batch_size: GPU batch 大小（use_batch=True 时生效）
        use_batch: 是否使用 GPU batch 推理

    Returns:
        包含输出视频 URL、总帧数、FPS、处理耗时等信息的字典
    """
    if not model_manager.is_available(model_key):
        raise ValueError(f"模型不可用: {model_key}")

    model = model_manager.get(model_key)

    # 打开视频
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise ValueError(f"无法打开视频: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width == 0 or height == 0:
        raise ValueError("无法读取视频尺寸")

    # 输出视频路径：原视频名_Hazydet.mp4
    output_filename = f"{input_path.stem}_Hazydet.mp4"
    output_path = RESULTS_VIDEOS_DIR / output_filename

    ffmpeg_exe = _get_ffmpeg_exe()
    use_ffmpeg = ffmpeg_exe is not None

    if use_ffmpeg:
        # 使用 imageio-ffmpeg 的 write_frames，输出浏览器可播放的 H.264 MP4
        from imageio_ffmpeg import write_frames
        writer = write_frames(
            str(output_path),
            (width, height),
            fps=fps,
            quality=7,  # 0-10，越高质量越好
            codec="libx264",
            pix_fmt_out="yuv420p",
            macro_block_size=1,  # 避免尺寸不是 16 倍数时出问题
        )
        writer.send(None)  # 初始化 generator
    else:
        writer = _create_opencv_writer(output_path, fps, width, height)

    start_time = time.time()
    processed_frames = 0
    saved_frames = 0
    last_detections: list = []

    # batch 模式使用的缓冲区
    frame_buffer: list[np.ndarray] = []
    index_buffer: list[int] = []
    result_cache: dict[int, list] = {}

    def _run_batch_inference():
        """对缓冲区中的帧进行 batch 推理，并缓存结果。"""
        nonlocal frame_buffer, index_buffer, result_cache
        if not frame_buffer:
            return

        if hasattr(model, "predict_batch"):
            results = model.predict_batch(frame_buffer)
        else:
            # fallback 到逐帧推理
            results = [model.predict_array(f) for f in frame_buffer]

        for idx, result in zip(index_buffer, results):
            detections, _ = parse_detection_results(result)
            result_cache[idx] = detections

        frame_buffer.clear()
        index_buffer.clear()

    def _write_frame(frame_idx: int, frame: np.ndarray):
        """根据缓存的检测结果在 frame 上画框并写入视频。"""
        nonlocal saved_frames, last_detections

        detections = result_cache.get(frame_idx, last_detections)
        if frame_idx in result_cache:
            last_detections = result_cache[frame_idx]
            del result_cache[frame_idx]

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plotted = draw_boxes_on_image(frame_rgb, detections)

        if use_ffmpeg:
            writer.send(plotted)
        else:
            output_frame = cv2.cvtColor(plotted, cv2.COLOR_RGB2BGR)
            writer.write(output_frame)

        saved_frames += 1

    # 预分配帧序号队列（用于延迟写入 batch 模式下的帧）
    pending_write_frames: list[tuple[int, np.ndarray]] = []

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frames += 1
            is_detect_frame = (processed_frames - 1) % detect_interval == 0

            if is_detect_frame:
                if use_batch:
                    frame_buffer.append(frame)
                    index_buffer.append(processed_frames)
                    if len(frame_buffer) >= batch_size:
                        _run_batch_inference()
                else:
                    result = model.predict_array(frame)
                    last_detections, _ = parse_detection_results(result)

            # batch 模式下，需要等检测结果缓存后才能写入
            if use_batch:
                pending_write_frames.append((processed_frames, frame))
                # 尝试写入 pending 队列中已有结果的帧
                while pending_write_frames:
                    idx, f = pending_write_frames[0]
                    if idx in result_cache or idx < processed_frames - batch_size * detect_interval - 5:
                        pending_write_frames.pop(0)
                        _write_frame(idx, f)
                    else:
                        break
            else:
                _write_frame(processed_frames, frame)

            # 进度回调
            if progress_callback and total_frames > 0:
                try:
                    progress_callback(processed_frames, total_frames)
                except Exception:
                    pass

            # 每处理一帧释放一下显存缓存
            if processed_frames % 30 == 0:
                try:
                    import torch
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                except Exception:
                    pass

        # 视频读取结束，flush 剩余 batch 和 pending 帧
        if use_batch:
            _run_batch_inference()
            while pending_write_frames:
                idx, f = pending_write_frames.pop(0)
                _write_frame(idx, f)

    finally:
        cap.release()
        if use_ffmpeg:
            try:
                writer.close()
            except Exception:
                pass
        else:
            writer.release()

    process_time = time.time() - start_time

    return {
        "video_url": f"/results/videos/{output_filename}",
        "filename": output_filename,
        "total_frames": saved_frames,
        "fps": round(fps, 2),
        "width": width,
        "height": height,
        "process_time": round(process_time, 2),
        "model": model_key,
        "detect_interval": detect_interval,
        "batch_size": batch_size if use_batch else 1,
        "use_batch": use_batch,
    }


def _create_opencv_writer(output_path: Path, fps: float, width: int, height: int):
    """使用 OpenCV 创建视频写入器（兼容性 fallback）。"""
    # 尝试 H.264 编码
    for codec in ("avc1", "H264", "mp4v"):
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        if writer.isOpened():
            return writer

    raise ValueError("无法创建输出视频文件，请安装 imageio-ffmpeg 或系统 ffmpeg")
