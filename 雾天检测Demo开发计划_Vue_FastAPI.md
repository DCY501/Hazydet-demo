# 雾天检测 Demo 开发计划（Vue 3 + FastAPI）

> 技术方案：Vue 3 + TypeScript + Vite + Element Plus + ECharts + FastAPI + Ultralytics  
> 目标：做一个精美的 Web 端雾天目标检测演示系统，支持单图检测、三模型对比、浓度鲁棒性分析、中间结果可视化、视频检测。

---

## 当前开发进展（截至 2026-06-18）

### ✅ 已完成

#### 后端
- [x] FastAPI 项目框架搭建（`backend/app/main.py`）
- [x] 模型管理器重构为工厂模式（`backend/app/models/`）
  - `base_model.py`：统一接口 `HazyDetModel`
  - `yolo_wrapper.py`：标准 YOLO 包装器（baseline）
  - `phase1_model.py`：方案一占位类（当前复用 baseline 权重）
  - `phase2_model.py`：方案二占位类（AFFM + RSM + RRAM）
  - `model_factory.py`：按 key 创建模型实例
- [x] 业务逻辑
  - `image_service.py`：单图检测、三模型对比、加雾合成、中间结果占位
  - `video_service.py`：视频逐帧检测（支持跳帧、GPU batch、ffmpeg 输出 H.264）
- [x] 所有 API 路由
  - `POST /api/detect`：单图检测（支持 `beta` 加雾参数）
  - `POST /api/compare`：三模型对比（支持 `beta` 加雾参数）
  - `POST /api/haze`：加雾合成
  - `POST /api/intermediate`：中间结果（占位，等待真实模型输出）
  - `POST /api/video`：视频检测（SSE 流式进度推送）
  - `GET /api/detect/models`：模型列表
- [x] 图像工具函数：`add_haze`、`draw_boxes_on_image`、`parse_detection_results`、`compute_metrics`、`save_upload_file` 等
- [x] CORS 配置修正
- [x] 修改版 Ultralytics 复制到 `backend/ultralytics/`，包含 AFFM/RSM/RRAM/DehazeHead 等自定义模块
- [x] 权重文件已就位（本地，不进 Git）
  - `baseline.pt` ← `dehaze-yolov8-main/runs/detect/baseline_5beta_subset50_50e/weights/best.pt`
  - `phase1.pt` ← 同上（暂时复用）
  - `phase2.pt` ← `dehaze-yolov8-main/runs/detect/dehaze_v2_affm_rsm_rram_subset50_d02_recon_only_b8/weights/best.pt`
- [x] `requirements.txt` 包含 `imageio-ffmpeg` 等依赖
- [x] `run.py` 开发启动脚本

#### 前端
- [x] Vue 3 + TypeScript + Vite + Element Plus 脚手架搭建
- [x] ECharts + vue-echarts 集成（柱状图、折线图）
- [x] 路由配置：Home / Detect / Compare / Robustness / Intermediate / Video / About
- [x] Pinia 状态管理（`stores/app.ts`），支持 `currentFile` 跨页面共享
- [x] Axios 请求封装（`api/request.ts`、`api/detect.ts`、`api/models.ts`）
- [x] 公共组件
  - `AppLayout.vue`：左侧菜单 + 顶部栏 + 折叠
  - `UploadBox.vue`：拖拽上传，支持图片/视频
  - `ModelSelector.vue`：模型选择下拉
  - `ResultCard.vue`：结果图 + 指标 + 检测列表
  - `ImageCompare.vue`：多图对比布局
- [x] 7 个页面全部完成
  - `Home.vue`：首页、模型状态、功能入口
  - `Detect.vue`：单图检测 + 结果展示 + 跳转入口
  - `Compare.vue`：三模型并排对比 + 指标柱状图
  - `Robustness.vue`：多 beta 浓度分析 + 折线图 + 汇总表
  - `Intermediate.vue`：方案一/方案二 Tab 切换 + 中间结果展示
  - `Video.vue`：视频上传 + SSE 进度条 + 结果播放/下载
  - `About.vue`：项目介绍、技术栈、方案演进
- [x] `npm run build` 编译通过
- [x] `npm run dev` 开发服务器可正常启动

#### 部署/工程
- [x] GitHub 仓库创建并推送：`https://github.com/DCY501/Hazydet-Demo`
- [x] `.gitignore` 配置完善
- [x] `README.md` 编写

### 🚧 待实现/待完善

#### 后端
- [ ] **中间结果真实提取**
  - `phase1_model.intermediate()`：返回真实 AOD-Net 去雾增强图
  - `phase2_model.intermediate()`：从模型中提取真实 Ĵ / t / A / reconstruction
- [ ] **模型加载验证**：在 `yolov8-haze` conda 环境中启动 `uvicorn`，确认三个模型都能正常加载
- [ ] **错误处理增强**：模型加载失败、推理异常时的友好返回
- [ ] **指标丰富**：mAP、FPS、参数量/计算量展示（可选）

#### 前端
- [ ] **UI 美化**：主题色统一、动画、响应式细节、空状态/错误状态处理
- [ ] **结果下载**：检测图、视频下载按钮（视频页面已有，图片页面可补充）
- [ ] **图片预览优化**：原图与结果图联动对比增强

#### 部署
- [ ] `deploy/nginx.conf` 与 `deploy/hazydet.service` 尚未创建
- [ ] 生产环境打包与部署验证

---

## 一、技术选型

### 前端

| 技术 | 版本/说明 | 用途 |
|---|---|---|
| Vue 3 | 3.4+ | 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 5.x | 构建工具 |
| Element Plus | 2.7+ | UI 组件库 |
| Vue Router | 4.x | 页面路由 |
| Pinia | 2.x | 状态管理 |
| Axios | 1.x | HTTP 请求 |
| ECharts | 6.x | 图表（置信度分布、指标对比、鲁棒性曲线） |
| vue-echarts | 8.x | ECharts Vue 组件 |
| @element-plus/icons-vue | 2.x | 图标 |

### 后端

| 技术 | 版本/说明 | 用途 |
|---|---|---|
| Python | 3.10+ | 运行环境 |
| FastAPI | 0.115+ | Web 框架 |
| Uvicorn | 0.34+ | ASGI 服务器 |
| Ultralytics | 8.x | YOLO 模型推理 |
| OpenCV | 4.x | 图像处理 |
| NumPy | 1.x | 数值计算 |
| Pillow | 10.x | 图像格式转换 |
| imageio-ffmpeg | 0.5+ | 视频编码为 H.264 MP4 |
| python-multipart | — | 文件上传支持 |

### 部署

| 组件 | 用途 |
|---|---|
| Nginx | 前端静态文件服务 + 反向代理 |
| systemd | 后端服务托管 |
| Ubuntu 22.04 | 服务器系统（可选，当前优先本地部署） |

---

## 二、项目结构

```
Hazydet-demo/
├── backend/                          # FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI 应用入口（优先加载本地 ultralytics）
│   │   ├── config.py                 # 配置（模型路径、结果目录、允许格式）
│   │   ├── models/                   # 模型结构（独立模块，便于并行开发和更换）
│   │   │   ├── __init__.py
│   │   │   ├── base_model.py         # HazyDetModel 统一接口
│   │   │   ├── yolo_wrapper.py       # 标准 YOLO 包装器（baseline）
│   │   │   ├── phase1_model.py       # 方案一占位类
│   │   │   ├── phase2_model.py       # 方案二占位类
│   │   │   └── model_factory.py      # 模型工厂
│   │   ├── routers/                  # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── detect.py             # 单图检测
│   │   │   ├── compare.py            # 三模型对比
│   │   │   ├── haze.py               # 加雾合成
│   │   │   ├── intermediate.py       # 中间结果
│   │   │   └── video.py              # 视频检测（SSE）
│   │   ├── services/                 # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── model_manager.py      # 模型加载/管理
│   │   │   ├── image_service.py      # 图片检测逻辑
│   │   │   └── video_service.py      # 视频检测逻辑
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── image_utils.py        # 图像工具（加雾、画框、解析结果等）
│   ├── ultralytics/                  # 修改版 Ultralytics（含 AFFM/RSM/RRAM 等自定义模块）
│   ├── weights/                      # 模型权重文件（.pt，本地，不进 Git）
│   │   ├── baseline.pt
│   │   ├── phase1.pt
│   │   └── phase2.pt
│   ├── results/                      # 检测结果输出（运行时生成）
│   │   ├── images/
│   │   └── videos/
│   ├── requirements.txt
│   └── run.py                        # 开发启动脚本
├── frontend/                         # Vue 3 前端
│   ├── src/
│   │   ├── api/                      # Axios 请求封装
│   │   │   ├── detect.ts
│   │   │   └── models.ts
│   │   ├── assets/                   # 静态资源
│   │   │   └── styles/
│   │   │       └── main.scss
│   │   ├── components/               # 公共组件
│   │   │   ├── AppLayout.vue
│   │   │   ├── UploadBox.vue
│   │   │   ├── ModelSelector.vue
│   │   │   ├── ResultCard.vue
│   │   │   └── ImageCompare.vue
│   │   ├── router/
│   │   │   └── index.ts
│   │   ├── stores/
│   │   │   └── app.ts                # Pinia 状态，含 currentFile 跨页面共享
│   │   ├── views/                    # 页面
│   │   │   ├── Home.vue
│   │   │   ├── Detect.vue
│   │   │   ├── Compare.vue
│   │   │   ├── Robustness.vue
│   │   │   ├── Intermediate.vue
│   │   │   ├── Video.vue
│   │   │   └── About.vue
│   │   ├── App.vue
│   │   ├── main.ts                   # ECharts 注册
│   │   └── env.d.ts
│   ├── public/
│   │   └── hazydet.svg
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   └── index.html
├── README.md
├── .gitignore
└── deploy/                           # 部署脚本（待创建）
    ├── nginx.conf
    └── hazydet.service
```

---

## 三、功能模块

### 3.1 首页（Home） ✅ 已完成

- 项目标题和简介
- 三个核心亮点卡片：多任务检测框架、5-beta 多浓度雾天数据、检测性能提升
- 快速入口按钮
- 模型状态显示（已接入 `/api/detect/models`）
- 左侧菜单导航

### 3.2 单图检测（Detect） ✅ 已完成

- 图片上传/拖拽
- 模型选择：baseline / 方案一 / 方案二
- 可选 `beta` 加雾
- 原图与结果图并排预览
- 检测指标：目标数、平均置信度、推理耗时
- 检测结果列表
- 跳转入口：三模型对比、方案一中间结果、方案二中间结果、浓度鲁棒性

### 3.3 三模型对比（Compare） ✅ 已完成

- 上传一张图片
- 可选 `beta` 加雾后对比
- 三个模型并排显示结果
- 每个模型显示：结果图、目标数、平均置信度、推理耗时、检出目标列表
- 底部指标对比柱状图（目标数/平均置信度/推理耗时）

### 3.4 浓度鲁棒性（Robustness） ✅ 已完成

- 上传清晰图
- 自定义 beta 范围和步长
- 对每个 beta 调用检测
- 展示结果图矩阵
- 目标数随 beta 变化折线图
- 指标汇总表格

### 3.5 中间结果可视化（Intermediate） 🚧 页面完成，后端待完善

展示各方案的中间输出，帮助理解模型为什么有效。

#### 方案一（AOD-Net 前置去雾）

- 输入：有雾图
- 中间输出：
  - **去雾增强图**：AOD-Net 输出的清晰化图像（当前为占位）
  - **检测结果图**：在去雾增强图上做检测的结果

#### 方案二（AFFM + RSM 多任务检测）

- 输入：有雾图
- 中间输出：
  - **清晰图 `Ĵ`**：RSM 预测的无雾图像（当前为占位）
  - **透射率图 `t`**：雾的浓度分布（当前为占位）
  - **大气光 `A`**：全局大气光颜色（当前为占位）
  - **重构图 `Ĵ·t + A·(1-t)`**：验证物理一致性（当前为占位）
  - **检测结果图**：最终检测输出

#### baseline

- 无中间结果，仅显示检测结果图。

### 3.6 视频检测（Video） ✅ 已完成

- 上传短视频（MP4/AVI/MOV）
- 选择模型
- 跳帧间隔配置（1-5）
- GPU batch 加速开关 + batch 大小选择
- SSE 实时进度推送
- 处理完成后播放结果视频
- 显示处理信息：总帧数、FPS、分辨率、处理耗时
- 下载结果视频

### 3.7 项目介绍（About） ✅ 已完成

- 方法简介
- 方案演进时间线
- 技术栈说明
- 待完善：实验指标表、团队成员

---

## 四、后端 API 设计

> 注意：实际实现中上传字段统一为 `file`，并增加了 `beta` 加雾参数。

### 4.1 单图检测

```http
POST /api/detect
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `file` | File | 图片文件 |
| `model` | String | `baseline` / `phase1` / `phase2` |
| `beta` | Float | 可选，雾浓度，不传或 0 则不加雾 |

返回：

```json
{
  "success": true,
  "model": "phase2",
  "result_url": "/results/images/phase2_xxx.jpg",
  "metrics": {
    "count": 12,
    "avg_conf": 0.72,
    "inference_ms": 23.5
  },
  "detections": [
    {"class_name": "car", "confidence": 0.89, "bbox": [100, 200, 300, 400]}
  ],
  "class_distribution": {"car": 5, "person": 3}
}
```

### 4.2 三模型对比

```http
POST /api/compare
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `file` | File | 图片文件 |
| `beta` | Float | 可选，雾浓度 |

返回：

```json
{
  "success": true,
  "results": {
    "baseline": {
      "name": "Baseline",
      "result_url": "/results/images/baseline_xxx.jpg",
      "metrics": {"count": 8, "avg_conf": 0.61, "inference_ms": 20.0},
      "detections": [...]
    },
    "phase1": {...},
    "phase2": {...}
  }
}
```

### 4.3 加雾合成

```http
POST /api/haze
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `file` | File | 清晰图片 |
| `beta` | Float | 雾浓度 |

返回：

```json
{
  "success": true,
  "haze_url": "/results/images/haze_xxx.jpg"
}
```

### 4.4 视频检测（SSE 流式）

```http
POST /api/video
Content-Type: multipart/form-data
Accept: text/event-stream
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `file` | File | 视频文件 |
| `model` | String | 模型名称 |
| `detect_interval` | Int | 跳帧间隔，每隔多少帧检测一次 |
| `use_batch` | Bool | 是否使用 GPU batch 推理 |
| `batch_size` | Int | GPU batch 大小 |

SSE 消息：

```text
data: {"type": "progress", "percent": 45, "current": 450, "total": 1000}

data: {"type": "complete", "result": {"video_url": "/results/videos/xxx_Hazydet.mp4", ...}}

data: {"type": "error", "error": "错误信息"}
```

完成结果：

```json
{
  "video_url": "/results/videos/xxx_Hazydet.mp4",
  "filename": "xxx_Hazydet.mp4",
  "total_frames": 1000,
  "fps": 25,
  "width": 1920,
  "height": 1080,
  "process_time": 12.5,
  "model": "phase2",
  "detect_interval": 2,
  "batch_size": 4,
  "use_batch": true
}
```

### 4.5 中间结果

```http
POST /api/intermediate
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `file` | File | 图片文件 |
| `model` | String | `baseline` / `phase1` / `phase2` |

返回：

```json
{
  "success": true,
  "model": "phase2",
  "result_url": "/results/images/phase2_xxx.jpg",
  "metrics": {"count": 12, "avg_conf": 0.72, "inference_ms": 23.5},
  "intermediate": {
    "jhat": "/results/images/phase2_xxx_jhat.jpg",
    "transmission": "/results/images/phase2_xxx_t.jpg",
    "atmosphere": "/results/images/phase2_xxx_a.jpg",
    "reconstruction": "/results/images/phase2_xxx_recon.jpg"
  }
}
```

不同模型返回的中间结果：

| 模型 | 中间结果 |
|---|---|
| `baseline` | 无 |
| `phase1` | `dehazed`：AOD-Net 去雾后的图像 |
| `phase2` | `jhat`（Ĵ）、`transmission`（t）、`atmosphere`（A）、`reconstruction` |

### 4.6 模型列表

```http
GET /api/detect/models
```

返回：

```json
{
  "success": true,
  "models": {
    "baseline": {
      "key": "baseline",
      "name": "Baseline",
      "description": "原始 YOLOv8n，无去雾增强",
      "available": true,
      "has_intermediate": false,
      "intermediate_types": []
    },
    "phase1": {...},
    "phase2": {...}
  }
}
```

---

## 五、开发里程碑

### Week 1：基础框架

| 天数 | 前端任务 | 后端任务 | 状态 |
|---|---|---|---|
| Day 1-2 | 搭建 Vue 3 + TS + Vite + Element Plus 项目；配置路由和布局 | 搭建 FastAPI 项目；实现模型管理器 | ✅ 已完成 |
| Day 3-4 | 实现图片上传组件；模型选择组件；结果展示组件 | 实现 `/api/detect` 单图检测接口 | ✅ 已完成 |
| Day 5-6 | 完成 Detect 单图检测页面 | 实现 `/api/compare` 三模型对比接口 | ✅ 已完成 |
| Day 7 | 联调 Detect + Compare 页面 | 联调接口；修复 bug | ✅ 已完成 |

### Week 2：核心功能

| 天数 | 前端任务 | 后端任务 | 状态 |
|---|---|---|---|
| Day 8-9 | 完成 Compare 三模型对比页面；添加指标柱状图 | 实现 `/api/haze` 加雾接口 | ✅ 已完成 |
| Day 10-11 | 完成 Robustness 浓度鲁棒性页面 | 实现 `/api/intermediate` 中间结果接口 | ✅ 页面完成，后端中间结果待真实提取 |
| Day 12-13 | 完成 Intermediate 中间结果可视化页面 | 调试中间结果输出（RSM 的 Ĵ/t/A） | 🚧 页面完成，后端待实现 |
| Day 14 | 完成 About 项目介绍页面 | 整理 API 文档 | ✅ 已完成 |

### Week 3：视频 + 部署

| 天数 | 前端任务 | 后端任务 | 状态 |
|---|---|---|---|
| Day 15-17 | 完成 Video 视频检测页面；进度条；结果播放 | 实现 `/api/video` 视频处理接口（SSE） | ✅ 已完成 |
| Day 18-19 | UI 美化：自定义主题、动画、响应式、loading 效果 | 中间结果真实提取；错误处理 | 🚧 中间结果待实现 |
| Day 20 | 部署测试；准备答辩样例图片/视频 | 部署后端服务；Nginx 配置 | 🚧 部署脚本待创建 |

---

## 六、关键实现细节

### 6.1 后端模型管理（工厂模式）

```python
# app/services/model_manager.py
from app.config import MODELS
from app.models import create_model

class ModelManager:
    def __init__(self):
        self._models = {}
        self._availability = {}
        self._load_models()

    def _load_models(self):
        for key, cfg in MODELS.items():
            path = cfg["path"]
            if path.exists():
                try:
                    self._models[key] = create_model(key, path)
                    self._availability[key] = True
                except Exception as e:
                    print(f"[ModelManager] 加载失败 {key}: {e}")
                    self._availability[key] = False

    def get(self, model_key: str):
        return self._models.get(model_key)

    def is_available(self, model_key: str) -> bool:
        return self._availability.get(model_key, False)

model_manager = ModelManager()
```

### 6.2 前端状态管理（跨页面共享文件）

```typescript
// stores/app.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const availableModels = ref<ModelInfo[]>([])
  const currentFile = ref<File | null>(null)
  const currentImageUrl = ref<string>('')

  async function fetchModels() { ... }

  function setCurrentFile(file: File | null) {
    if (currentFile.value && currentImageUrl.value) {
      URL.revokeObjectURL(currentImageUrl.value)
    }
    currentFile.value = file
    currentImageUrl.value = file ? URL.createObjectURL(file) : ''
  }

  function clearCurrentFile() { ... }

  return {
    availableModels,
    currentFile,
    currentImageUrl,
    fetchModels,
    setCurrentFile,
    clearCurrentFile,
  }
})
```

### 6.3 视频检测 SSE 进度推送

后端：

```python
# app/routers/video.py
from fastapi.responses import StreamingResponse

@router.post("")
async def detect_video_endpoint(file: UploadFile, model: str, ...):
    async def event_stream():
        # 在后台线程运行同步视频检测
        task = loop.run_in_executor(None, run_detect)
        while not task.done():
            await asyncio.sleep(0.5)
            yield f"data: {json.dumps(progress)}\n\n"
        # 发送完成或错误消息
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

前端：

```typescript
// views/Video.vue
async function startVideoStream(formData: FormData) {
  const response = await fetch('/api/video', { method: 'POST', body: formData })
  const reader = response.body!.getReader()
  // 解析 SSE 数据，更新进度条和结果
}
```

### 6.4 响应式布局

页面采用 Element Plus 的栅格系统：

```vue
<el-row :gutter="20">
  <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
    <!-- baseline 结果 -->
  </el-col>
  <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
    <!-- 方案一结果 -->
  </el-col>
  <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
    <!-- 方案二结果 -->
  </el-col>
</el-row>
```

### 6.5 图片预览

上传图片后使用 `URL.createObjectURL` 本地预览，不需要先传到后端。

---

## 七、部署方案

### 7.1 后端部署

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

或使用 `run.py`：

```bash
python run.py
```

生产环境：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

### 7.2 前端部署

```bash
cd frontend
npm install
npm run build
```

产物在 `frontend/dist/`。

### 7.3 Nginx 配置（待创建）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/hazydet-demo/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
        proxy_buffering off;  # SSE 需要关闭缓冲
    }

    location /results/ {
        alias /opt/hazydet-demo/backend/results/;
    }
}
```

### 7.4 systemd 服务（待创建）

```ini
[Unit]
Description=Hazy Detection Demo Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/hazydet-demo/backend
ExecStart=/opt/hazydet-demo/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 八、答辩准备

### 8.1 准备演示样例

提前准备 5-10 张不同浓度、不同场景的有雾图片：

- 城市道路（车、行人）
- 远景目标
- 小目标
- 浓雾场景
- 轻雾场景

### 8.2 准备对比视频

准备 2-3 段短视频：

- 10 秒左右
- 有雾
- 能明显看出 baseline 漏检、我们的方法检出更多

### 8.3 准备答辩话术

- 首页：介绍问题背景和方案演进
- 对比页：核心亮点，三模型并排对比
- 鲁棒性页：展示对不同浓度雾的稳定检测
- 中间结果页：解释模型为什么有效
- 视频页：展示实时处理能力

---

## 九、下一步建议

1. **验证后端启动**：在 `yolov8-haze` conda 环境中启动 `uvicorn`，确认三个模型都能加载成功
2. **完善中间结果**：实现 `phase1_model.intermediate()` 和 `phase2_model.intermediate()` 的真实输出
3. **UI 美化与细节**：统一主题、动画、响应式、错误状态
4. **部署脚本**：创建 `deploy/nginx.conf` 和 `deploy/hazydet.service`
5. **准备答辩样例**：挑选和标注演示图片/视频
