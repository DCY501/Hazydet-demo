# Hazydet Demo 后端

基于 FastAPI + Ultralytics 的雾天目标检测演示后端。

## 快速开始

### 1. 创建虚拟环境（推荐）

```bash
cd Hazydet-demo/backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 放置模型权重

将训练好的 `.pt` 权重文件放到 `weights/` 目录下：

```
weights/
├── baseline.pt    # 原始 YOLOv8n
├── phase1.pt      # 方案一：AOD-Net 前置去雾
└── phase2.pt      # 方案二：AFFM + RSM 多任务检测
```

**注意**：权重文件名要和 `app/config.py` 里 `MODELS` 配置中的 `path` 一致。如果文件名不同，修改 `config.py` 即可，不需要改业务代码。

### 4. 启动服务

```bash
python run.py
```

服务启动后访问：

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health
- 模型列表：http://localhost:8000/api/detect/models

## API 列表

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/health` | GET | 健康检查 |
| `/api/detect/models` | GET | 获取可用模型列表 |
| `/api/detect` | POST | 单图检测 |
| `/api/compare` | POST | 三模型对比 |
| `/api/intermediate` | POST | 中间结果可视化 |
| `/api/haze/synthesize` | POST | 加雾合成 |
| `/api/video/detect` | POST | 视频检测（开发中） |

## 模型配置

模型信息统一在 `app/config.py` 中管理：

```python
MODELS = {
    "baseline": {
        "name": "Baseline",
        "path": WEIGHTS_DIR / "baseline.pt",
        "description": "原始 YOLOv8n，无去雾增强",
        "has_intermediate": False,
    },
    "phase1": {
        "name": "方案一",
        "path": WEIGHTS_DIR / "phase1.pt",
        "description": "AOD-Net 前置去雾 + YOLOv8 检测",
        "has_intermediate": True,
        "intermediate_types": ["dehazed"],
    },
    "phase2": {
        "name": "方案二",
        "path": WEIGHTS_DIR / "phase2.pt",
        "description": "AFFM + RSM 多任务检测框架",
        "has_intermediate": True,
        "intermediate_types": ["clear", "transmission", "atmosphere", "reconstruction"],
    },
}
```

只要替换 `weights/` 下的文件，或修改这里的 `path`，后端就能自动加载可用模型。

## 中间结果说明

| 模型 | 中间结果字段 | 含义 |
|---|---|---|
| baseline | 无 | 纯检测模型 |
| phase1 | `dehazed` | AOD-Net 去雾增强后的图像 |
| phase2 | `clear` | RSM 预测的清晰图 Ĵ |
| phase2 | `transmission` | 透射率图 t |
| phase2 | `atmosphere` | 大气光 A |
| phase2 | `reconstruction` | 重构图 Ĵ·t + A·(1-t) |

phase2 的中间结果提取逻辑后续在 `app/services/image_service.py` 的 `get_intermediate_results` 函数中实现，当前为占位。
