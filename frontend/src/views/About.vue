<template>
  <div class="about-page">
    <el-row justify="center">
      <el-col :xs="24" :md="18" :lg="14">
        <el-card shadow="never" class="about-card">
          <template #header>
            <h2>关于 Hazydet Demo</h2>
          </template>

          <p>
            <strong>Hazydet Demo</strong> 是一个面向雾天场景的目标检测 Web 演示系统，
            基于 YOLOv8 与去雾辅助多任务学习实现，用于课程设计与论文实验的可视化展示。
          </p>

          <el-divider content-position="left">核心方案</el-divider>

          <el-timeline>
            <el-timeline-item type="primary" :hollow="true">
              <h4>Baseline：YOLOv8n</h4>
              <p>原始 YOLOv8n 检测器，作为对比基线。</p>
            </el-timeline-item>
            <el-timeline-item type="success" :hollow="true">
              <h4>Phase 1：AOD-Net 前置去雾增强</h4>
              <p>先用 AOD-Net 对雾天图像进行去雾增强，再送入 YOLOv8 进行检测。</p>
            </el-timeline-item>
            <el-timeline-item type="warning" :hollow="true">
              <h4>Phase 2：AFFM + RSM 多任务检测</h4>
              <p>自适应特征融合模块（AFFM）与复原子网（RSM）联合训练，端到端去雾检测。</p>
            </el-timeline-item>
          </el-timeline>

          <el-divider content-position="left">技术栈</el-divider>

          <el-descriptions :column="2" border>
            <el-descriptions-item label="前端">Vue 3 + TypeScript + Vite + Element Plus</el-descriptions-item>
            <el-descriptions-item label="后端">FastAPI + Ultralytics + OpenCV</el-descriptions-item>
            <el-descriptions-item label="检测框架">YOLOv8</el-descriptions-item>
            <el-descriptions-item label="去雾方法">AOD-Net / AFFM / RSM</el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">作者</el-divider>
          <p>本项目为课程设计/论文实验演示用途。</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.about-page {
  .about-card {
    border-radius: 12px;

    h2 {
      margin: 0;
      color: #1e293b;
    }

    p {
      line-height: 1.8;
      color: #475569;
    }

    h4 {
      margin: 0 0 4px;
      color: #334155;
    }
  }
}
</style>
