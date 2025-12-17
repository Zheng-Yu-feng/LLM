# model_manager/base_model.py
from abc import ABC, abstractmethod

class ChatModel(ABC):
    @abstractmethod
    def load(self): pass

    @abstractmethod
    def generate_response(self, messages, temperature=1.0, top_p=1.0, top_k=50, max_length=1024): 
        """
        核心对话方法，统一接受可调参数
        """
        pass
    # def set_parameters(self, params: dict):
    #     pass  # 可选，不是所有模型都支持
