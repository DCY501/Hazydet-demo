# 雾天检测 Demo 开发计划（Vue 3 + FastAPI）

> 技术方案：Vue 3 + TypeScript + Vite + Element Plus + FastAPI + Ultralytics  
> 开发周期：20 天  
> 目标：做一个精美的 Web 端雾天目标检测演示系统，支持图片三模型对比、中间结果可视化、视频检测。

---

## 一、技术选型

### 前端

| 技术 | 版本/说明 | 用途 |
|---|---|---|
| Vue 3 | 3.5+ | 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 6.x | 构建工具 |
| Element Plus | 2.13+ | UI 组件库 |
| Vue Router | 4.x | 页面路由 |
| Pinia | 2.x | 状态管理 |
| Axios | 1.x | HTTP 请求 |
| ECharts | 5.x | 图表（置信度分布、指标对比） |
| @element-plus/icons-vue | — | 图标 |

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
| python-multipart | — | 文件上传支持 |

### 部署

| 组件 | 用途 |
|---|---|
| Nginx | 前端静态文件服务 + 反向代理 |
| systemd | 后端服务托管 |
| Ubuntu 22.04 | 服务器系统 |

---

## 二、项目结构

```
Hazydet-demo/
├── backend/                          # FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI 应用入口
│   │   ├── config.py                 # 配置（模型路径、结果目录）
│   │   ├── routers/                  # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── detect.py             # 单模型检测
│   │   │   ├── compare.py            # 三模型对比
│   │   │   ├── haze.py               # 加雾合成
│   │   │   └── video.py              # 视频检测
│   │   ├── services/                 # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── model_manager.py      # 模型加载/管理
│   │   │   ├── image_service.py      # 图片检测逻辑
│   │   │   └── video_service.py      # 视频检测逻辑
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── image_utils.py        # 图像工具（加雾、画框等）
│   ├── weights/                      # 模型权重
│   │   ├── baseline.pt
│   │   ├── phase1.pt
│   │   └── phase2.pt
│   ├── results/                      # 检测结果输出
│   │   ├── images/
│   │   └── videos/
│   ├── requirements.txt
│   └── run.py                        # 启动脚本
├── frontend/                         # Vue 3 前端
│   ├── src/
│   │   ├── api/                      # Axios 请求封装
│   │   │   ├── detect.ts
│   │   │   ├── compare.ts
│   │   │   └── video.ts
│   │   ├── assets/                   # 静态资源
│   │   │   ├── logo.png
│   │   │   └── styles/
│   │   │       └── variables.scss
│   │   ├── components/               # 公共组件
│   │   │   ├── ImageUploader.vue
│   │   │   ├── DetectionResult.vue
│   │   │   ├── ModelSelector.vue
│   │   │   ├── MetricCard.vue
│   │   │   └── CompareLayout.vue
│   │   ├── router/
│   │   │   └── index.ts
│   │   ├── stores/
│   │   │   └── demoStore.ts
│   │   ├── views/                    # 页面
│   │   │   ├── HomeView.vue          # 首页
│   │   │   ├── DetectView.vue        # 单模型检测
│   │   │   ├── CompareView.vue       # 三模型对比
│   │   │   ├── RobustnessView.vue    # 浓度鲁棒性
│   │   │   ├── IntermediateView.vue  # 中间结果
│   │   │   ├── VideoView.vue         # 视频检测
│   │   │   └── AboutView.vue         # 项目介绍
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
├── README.md
└── deploy/                           # 部署脚本
    ├── nginx.conf
    └── hazydet.service
```

---

## 三、功能模块

### 3.1 首页（Home）

- 项目标题和简介
- 三个核心亮点卡片：
  - 多任务检测框架
  - 5-beta 多浓度雾天数据
  - 检测性能提升
- 快速入口按钮
- 技术路线图

### 3.2 单图检测（Detect）

- 图片上传/拖拽
- 模型选择：baseline / 方案一 / 方案二
- 原图预览
- 检测结果图（带 bbox、类别、置信度）
- 检测指标：目标数、平均置信度、类别分布
- 检测结果列表

### 3.3 三模型对比（Compare）★核心

- 上传一张图片
- 三个模型并排显示结果
- 每个模型显示：
  - 结果图
  - 目标数
  - 平均置信度
  - 检出目标列表
- 底部汇总表格/柱状图对比

### 3.4 浓度鲁棒性（Robustness）

- 上传清晰图
- 一键生成 5 种 beta 浓度的雾图
- 对每种浓度用方案二检测
- 展示 5 张结果图
- 绘制目标数随 beta 变化曲线

### 3.5 中间结果可视化（Intermediate）

展示各方案的中间输出，帮助理解模型为什么有效。

#### 方案一（AOD-Net 前置去雾）

- 输入：有雾图
- 中间输出：
  - **去雾增强图**：AOD-Net 输出的清晰化图像
  - **检测结果图**：在去雾增强图上做检测的结果

#### 方案二（AFFM + RSM 多任务检测）

- 输入：有雾图
- 中间输出：
  - **透射率图 `t`**：雾的浓度分布，越亮表示透射率越高（雾越淡）
  - **清晰图 `Ĵ`**：RSM 预测的无雾图像
  - **大气光 `A`**：全局大气光颜色，以颜色块 + RGB 数值显示
  - **重构图 `Ĵ·t + A·(1-t)`**：验证物理一致性
  - **检测结果图**：最终检测输出

#### baseline

- 无中间结果，仅显示检测结果图。

### 3.6 视频检测（Video）

- 上传短视频
- 选择模型
- 后端逐帧处理
- 显示处理进度条
- 播放结果视频
- 下载结果视频

### 3.7 项目介绍（About）

- 方法简介
- 网络架构图
- 实验指标表
- 团队成员

---

## 四、后端 API 设计

### 4.1 单图检测

```http
POST /api/detect
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `image` | File | 图片文件 |
| `model` | String | `baseline` / `phase1` / `phase2` |

返回：

```json
{
  "success": true,
  "model": "phase2",
  "result_url": "/results/images/phase2_xxx.jpg",
  "count": 12,
  "avg_confidence": 0.72,
  "detections": [
    {"class": "car", "confidence": 0.89, "bbox": [100, 200, 300, 400]}
  ],
  "class_distribution": {"car": 5, "person": 3, ...}
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
| `image` | File | 图片文件 |

返回：

```json
{
  "success": true,
  "results": {
    "baseline": {
      "result_url": "/results/images/baseline_xxx.jpg",
      "count": 8,
      "avg_confidence": 0.61,
      "detections": [...]
    },
    "phase1": {...},
    "phase2": {...}
  }
}
```

### 4.3 加雾合成

```http
POST /api/haze/synthesize
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `image` | File | 清晰图片 |
| `beta` | Float | 雾浓度 |

返回：

```json
{
  "success": true,
  "haze_url": "/results/images/haze_xxx.jpg"
}
```

### 4.4 视频检测

```http
POST /api/video/detect
Content-Type: multipart/form-data
```

参数：

| 字段 | 类型 | 说明 |
|---|---|---|
| `video` | File | 视频文件 |
| `model` | String | 模型名称 |

返回（异步或同步）：

```json
{
  "success": true,
  "task_id": "xxx",
  "status": "processing"
}
```

查询进度：

```http
GET /api/video/status/{task_id}
```

返回结果：

```json
{
  "success": true,
  "status": "completed",
  "result_url": "/results/videos/output_xxx.mp4",
  "fps": 15,
  "duration": 10
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
| `image` | File | 图片文件 |
| `model` | String | `baseline` / `phase1` / `phase2` |

返回：

```json
{
  "success": true,
  "model": "phase2",
  "result_url": "/results/images/phase2_xxx.jpg",
  "intermediate": {
    "clear": "/results/images/phase2_xxx_j.jpg",
    "transmission": "/results/images/phase2_xxx_t.jpg",
    "atmosphere": [0.75, 0.78, 0.80],
    "reconstruction": "/results/images/phase2_xxx_recon.jpg"
  }
}
```

不同模型返回的中间结果：

| 模型 | 中间结果 |
|---|---|
| `baseline` | 无 |
| `phase1` | `dehazed`：AOD-Net 去雾后的图像 |
| `phase2` | `clear`（Ĵ）、`transmission`（t）、`atmosphere`（A）、`reconstruction` |

---

## 五、20 天开发里程碑

### Week 1：基础框架（第 1-7 天）

| 天数 | 前端任务 | 后端任务 |
|---|---|---|
| Day 1-2 | 搭建 Vue 3 + TS + Vite + Element Plus 项目；配置路由和布局 | 搭建 FastAPI 项目；实现模型管理器；加载三个模型 |
| Day 3-4 | 实现图片上传组件；模型选择组件；结果展示组件 | 实现 `/api/detect` 单图检测接口 |
| Day 5-6 | 完成 Detect 单图检测页面 | 实现 `/api/compare` 三模型对比接口 |
| Day 7 | 联调 Detect + Compare 页面 | 联调接口；修复 bug |

### Week 2：核心功能（第 8-14 天）

| 天数 | 前端任务 | 后端任务 |
|---|---|---|
| Day 8-9 | 完成 Compare 三模型对比页面；添加指标卡片和柱状图 | 实现 `/api/haze/synthesize` 加雾接口 |
| Day 10-11 | 完成 Robustness 浓度鲁棒性页面 | 实现 `/api/intermediate` 中间结果接口 |
| Day 12-13 | 完成 Intermediate 中间结果可视化页面 | 调试中间结果输出（RSM 的 Ĵ/t/A） |
| Day 14 | 完成 About 项目介绍页面 | 整理 API 文档 |

### Week 3：视频 + 美化（第 15-20 天）

| 天数 | 前端任务 | 后端任务 |
|---|---|---|
| Day 15-17 | 完成 Video 视频检测页面；进度条；结果播放 | 实现 `/api/video/detect` 视频处理接口 |
| Day 18-19 | UI 美化：自定义主题、动画、响应式、 loading 效果 | 视频接口优化；错误处理 |
| Day 20 | 部署测试；准备答辩样例图片/视频 | 部署后端服务；Nginx 配置 |

---

## 六、关键实现细节

### 6.1 后端模型管理

```python
# app/services/model_manager.py
from ultralytics import YOLO
from functools import lru_cache

class ModelManager:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self):
        self.models["baseline"] = YOLO("weights/baseline.pt")
        self.models["phase1"] = YOLO("weights/phase1.pt")
        self.models["phase2"] = YOLO("weights/phase2.pt")
    
    def get(self, name: str) -> YOLO:
        return self.models.get(name)

model_manager = ModelManager()
```

### 6.2 前端状态管理

```typescript
// stores/demoStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDemoStore = defineStore('demo', () => {
  const currentImage = ref<string>('')
  const selectedModel = ref<string>('phase2')
  const detectionResult = ref<any>(null)
  const compareResult = ref<any>(null)
  
  return {
    currentImage,
    selectedModel,
    detectionResult,
    compareResult
  }
})
```

### 6.3 响应式布局

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

### 6.4 图片预览

上传图片后使用 `URL.createObjectURL` 本地预览，不需要先传到后端。

---

## 七、部署方案

### 7.1 后端部署

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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

### 7.3 Nginx 配置

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
    }

    location /results/ {
        alias /opt/hazydet-demo/backend/results/;
    }
}
```

### 7.4 systemd 服务

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
- 对比页：这是我们的核心亮点
- 鲁棒性页：展示对不同浓度雾的稳定检测
- 中间结果页：解释模型为什么有效

---

## 九、我可以帮你做的

1. **后端完整代码**：FastAPI 项目、模型管理、所有 API 接口
2. **前端核心组件**：上传组件、对比布局、结果展示、图表
3. **项目初始化**：Vue 3 + Vite + Element Plus 脚手架
4. **部署脚本**：Nginx 配置、systemd 服务
5. **Bug 调试**：训练/推理/前后端联调问题
6. **UI 美化建议**：布局、配色、动画

你可以选择一个起点，我们开始写代码。建议先从**后端单图检测 API** 开始，因为它是一切功能的基础。
