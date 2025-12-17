from transformers import pipeline
from .base_model import ChatModel
import torch

class ZephyrModel(ChatModel):
    def load(self):
        self.pipe = pipeline("text-generation", model="zephyr", torch_dtype="auto", device_map="auto")

    def generate_response(self, history, temperature=1.0, top_p=1.0, top_k=50, max_length=1024):
        with torch.no_grad():
            prompt = self.pipe.tokenizer.apply_chat_template(history, tokenize=False, add_generation_prompt=True)
            outputs = self.pipe(prompt, max_new_tokens=max_length, do_sample=True, temperature=temperature, top_k=top_k, top_p=top_p)
        #response = outputs[0]["generated_text"].split("</s>")[-1].strip()  
        response = outputs[0]["generated_text"].split("<|assistant|>", 1)[1].strip()
        return response
