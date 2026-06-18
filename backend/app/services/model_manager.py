"""
模型管理器

负责按需加载检测模型。只有权重文件存在时才会加载，
不存在的模型会在 API 中标记为不可用。

新增模型方案时：
    1. 在 app.models 下实现继承 HazyDetModel 的类
    2. 在 app.models.model_factory 中注册
    3. 在 app.config.MODELS 中添加配置
"""
from app.config import MODELS
from app.models import create_model


class ModelManager:
    """管理所有检测模型，按需加载。"""

    def __init__(self):
        self._models = {}
        self._availability = {}
        self._load_models()

    def _load_models(self):
        """遍历配置，加载存在的模型。"""
        for key, cfg in MODELS.items():
            path = cfg["path"]
            if path.exists():
                try:
                    print(f"[ModelManager] 加载模型: {key} -> {path}")
                    self._models[key] = create_model(key, path)
                    self._availability[key] = True
                except Exception as e:
                    print(f"[ModelManager] 加载失败 {key}: {e}")
                    self._availability[key] = False
            else:
                print(f"[ModelManager] 权重不存在，跳过: {key} -> {path}")
                self._availability[key] = False

    def get(self, model_key: str):
        """获取已加载的模型实例。"""
        return self._models.get(model_key)

    def is_available(self, model_key: str) -> bool:
        """检查模型是否可用。"""
        return self._availability.get(model_key, False)

    def available_models(self) -> dict:
        """返回所有已配置模型的信息及可用状态。"""
        result = {}
        for key, cfg in MODELS.items():
            result[key] = {
                "key": key,
                "name": cfg["name"],
                "description": cfg["description"],
                "available": self._availability.get(key, False),
                "has_intermediate": cfg.get("has_intermediate", False),
                "intermediate_types": cfg.get("intermediate_types", []),
            }
        return result

    def model_names(self) -> list:
        """返回可用模型的 key 列表。"""
        return [k for k, v in self._availability.items() if v]


# 全局单例
model_manager = ModelManager()
