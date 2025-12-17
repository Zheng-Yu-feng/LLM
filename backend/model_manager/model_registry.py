# model_manager/model_registry.py
from .baichuan2_model import Baichuan2Model
from .qwen3_model import QwenModel
from .yi_model import YiModel
from .mistral_model import MistralModel
from .ge_model import GeModel
from .zephyr_model import ZephyrModel
model_classes = {
    "百川": Baichuan2Model,
    "通义千问": QwenModel,
    "Yi": YiModel,
    "九格": GeModel,
    "mistral": MistralModel,
    "zephyr": ZephyrModel
}
model_apis = {
    "deepseek": "https://api.deepseek.com",
}