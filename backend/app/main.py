"""
Hazydet Demo 后端入口
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import RESULTS_DIR
from app.routers import compare, detect, haze, intermediate, video


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理。"""
    print("[Hazydet Demo] 服务启动")
    yield
    print("[Hazydet Demo] 服务关闭")


app = FastAPI(
    title="Hazydet Demo API",
    description="雾天目标检测演示系统后端 API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 配置，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载结果文件目录为静态文件
app.mount("/results", StaticFiles(directory=str(RESULTS_DIR)), name="results")

# 注册路由
app.include_router(detect.router, prefix="/api")
app.include_router(compare.router, prefix="/api")
app.include_router(intermediate.router, prefix="/api")
app.include_router(haze.router, prefix="/api")
app.include_router(video.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    """健康检查接口。"""
    return {"status": "ok", "service": "hazydet-demo"}


@app.get("/")
async def root():
    """根路径重定向到 API 文档。"""
    return {
        "message": "Hazydet Demo API",
        "docs": "/docs",
    }
