# Hazydet Demo

基于 YOLOv8 与去雾辅助多任务学习的雾天目标检测 Web 演示系统。

## 项目结构

```
Hazydet-demo/
├── backend/          # FastAPI 后端
│   ├── app/          # 应用代码
│   │   ├── config.py # 模型路径配置
│   │   ├── main.py   # FastAPI 入口
│   │   ├── routers/  # API 路由
│   │   ├── services/ # 业务逻辑
│   │   └── utils/    # 工具函数
│   ├── weights/      # 模型权重文件（.pt）
│   ├── results/      # 检测结果输出（运行时生成）
│   └── requirements.txt
├── frontend/         # Vue 3 + TypeScript + Vite 前端
│   ├── src/
│   │   ├── api/      # 接口请求
│   │   ├── components/ # 通用组件
│   │   ├── router/   # 路由
│   │   ├── stores/   # Pinia 状态管理
│   │   ├── views/    # 页面
│   │   └── assets/   # 样式与静态资源
│   └── package.json
└── README.md
```

## 功能

- **单图检测**：上传图片，选择模型，查看检测结果与指标
- **三模型对比**：同一张图同时对比 baseline / phase1 / phase2
- **浓度鲁棒性**：模拟不同雾浓度 β，观察模型性能变化
- **中间结果可视化**：查看去雾图、透射率、重构图等中间结果
- **视频检测**：上传视频并查看逐帧检测结果

## 快速开始

### 1. 放置模型权重

将 `.pt` 权重文件放入 `backend/weights/`：

```
backend/weights/
├── baseline.pt
├── phase1.pt
└── phase2.pt
```

代码中的模型路径在 `backend/app/config.py` 中配置，替换权重文件无需修改代码。

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器访问 http://localhost:5173。

## 部署

开发调试用上述命令即可。如需打包成品：

```bash
cd frontend
npm run build
```

构建产物位于 `frontend/dist/`，可用 Nginx 或任意静态服务器托管。

## 注意事项

- 当前只有 `baseline` 权重时，phase1/phase2 相关页面会提示模型不可用。
- 视频检测接口目前为占位实现，后续补充完整逻辑。
- 中间结果提取逻辑依赖具体模型结构，后续根据 phase1/phase2 实现完善。
