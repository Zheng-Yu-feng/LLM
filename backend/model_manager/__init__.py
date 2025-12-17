# model_manager/__init__.py
import torch
from .model_registry import model_classes,model_apis
from collections import defaultdict
from extensions import db
from models import Message
import requests
from openai import OpenAI
DEFAULT_MODEL_NAME = "九格"

class ModelManager:
    def __init__(self):
        torch.cuda.empty_cache()
        self.current_name = None
        self.current_instance = None
        # 每个用户 -> 消息历史
        #self.user_histories = defaultdict(list)
        self.parameters = {
            "temperature": 1.0,
            "top_p": 1.0,
            "top_k": 20,
            "max_length": 1024
        }
        self.max_history = 20
        self.set_model(DEFAULT_MODEL_NAME)
        self.system_prompt = {
            "role": "system",
            # "content": "You are an English teacher AI assistant. You are from a company named Alfaright(阿尔法睿). Your only role is to help users with English language learning and answer questions related to English. Please only respond to queries about English language, grammar, vocabulary, pronunciation, or English learning strategies. If a user asks about topics unrelated to English, politely decline to answer and remind them that you're here to assist with English-related questions only."
            # "content": "You are an English teacher AI assistant. Your name is Alfaright(Chinese name 阿尔法睿). Your role is strictly limited to helping users with English language learning. You must only respond to queries about English language, grammar, vocabulary, pronunciation, or English learning strategies. If a user asks about any topic unrelated to English learning, you must refuse to answer and respond only in English with: 'I'm sorry, but I can only assist with English-related questions. Could you please ask something about English language or learning?'"
            "content": "请你对我说的内容做出回答"
        }
        self.model_classes_api = model_apis
        self.model_classes = model_classes
        self.api_model ="deepseek"
        self.api_url = "https://api.deepseek.com"
        self.api_key = ""
    def set_model(self, name: str):
        if name == self.current_name:
            return  # 无需切换

        if name not in model_classes:
            raise ValueError(f"不支持的模型：{name}")

        # 清理旧模型
        if self.current_instance:
            del self.current_instance
            torch.cuda.empty_cache()

        # 加载新模型
        instance = model_classes[name]()
        instance.load()
        self.current_name = name
        self.current_instance = instance

    def generate_response(self, history,new_messages):
        if not self.current_instance:
            raise RuntimeError("未加载任何模型")
        # if user_id not in self.user_histories:
        #     self.user_histories[user_id] = [self.system_prompt]
        # history = self.user_histories[user_id]
        history.extend([new_messages])
        
        # history = history[:][-self.max_history:]
        # print(f"history:{history}")
        
        response = self.current_instance.generate_response(history,**self.parameters)
        # history.append({'role': 'assistant', 'content': response})
        # self.user_histories[user_id] = history
        
        #写入数据库--------------------------------------------
        # db.session.add(Message(
        #     user_id=user_id, role=new_messages['role'],
        #     content=new_messages['content']
        # ))
        # db.session.add(Message(
        #     user_id=user_id, role='assistant',
        #     content=response
        # ))
        # db.session.commit()
        #-----------------------------------------------------
        return response

    def set_parameters(self, temperature=None, top_p=None, max_length=None, top_k=None, thinking=None):
        # 更新 temperature
        if temperature is not None:
            self.parameters["temperature"] = temperature
        
        # 更新 top_p
        if top_p is not None:
            self.parameters["top_p"] = top_p
        
        # 更新 max_length
        if max_length is not None:
            self.parameters["max_length"] = max_length
        
        # 更新 top_k
        if top_k is not None:
            self.parameters["top_k"] = top_k

        # if thinking is not None:
        #     # 假设 "thinking" 参数需要特殊处理
        #     self.parameters["thinking"] = thinking
        print(f"Updated parameters: {self.parameters}")
    
    def upload_file(self, user_id, text):
        # self.user_histories[user_id].append[{"role": "system", "content": "解析以下内容:\n"+text}]
        self.user_histories[user_id].append({"role": "user", "content": "解析以下内容:\n"+text})
        print("文件上传成功")
        print(f"after upload history:{self.user_histories[user_id]}")

    def set_api(self, api_model):
        self.api_model = api_model
        self.api_url = self.model_classes_api[api_model]
        #self.api_key = self.api_key
        print("API设置成功")

    import requests

    def call_api_chat(self, messages, params=None):
        """
        调用第三方 Chat API。
        出现错误时，直接返回中文提示字符串，方便前端展示。
        """

        # 1. 基础配置检查：API 地址 / 密钥 / 模型
        if not getattr(self, "api_url", None):
            return "API 地址未配置，请先在后台配置正确的 API URL。"

        if not getattr(self, "api_key", None):
            return "未检测到 API 密钥，请先在设置中填写有效的密钥。"

        if not getattr(self, "api_model", None):
            return "未选择任何 API 模型，请在顶部栏选择模型后重试。"
        try:
            client = client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_url,
            )
            
            response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=self.parameters["temperature"],
            max_tokens=self.parameters["max_length"],
            )
            response = response.choices[0].message.content
        except Exception as e:
            return f"调用 API 时发生错误,请检查"
        return response



