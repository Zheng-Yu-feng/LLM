# model_manager/baichuan2_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from .base_model import ChatModel
import torch
from transformers.generation.utils import GenerationConfig

class Baichuan2Model(ChatModel):
    def load(self):

        self.tokenizer = AutoTokenizer.from_pretrained("baichuan", use_fast=False, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained("baichuan", device_map="auto", torch_dtype="auto", trust_remote_code=True).eval()
        #self.model.generation_config = GenerationConfig.from_pretrained("baichuan")
        self.config = GenerationConfig.from_pretrained("baichuan")

    def generate_response(self, history, temperature=1.0, top_p=1.0, top_k=50, max_length=1024):

        self.config.temperature = temperature
        self.config.top_p = top_p
        self.config.top_k = top_k
        self.config.max_new_tokens = max_length
        self.model.generation_config = self.config
        with torch.no_grad():
            response = self.model.chat(self.tokenizer,history)

        return response
