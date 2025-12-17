from transformers import AutoModelForCausalLM, AutoTokenizer
from .base_model import ChatModel
import torch

class GeModel(ChatModel):
    def load(self):
        model_path = "9G7B_MHA" 
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            device_map="auto",
            torch_dtype='auto',
            trust_remote_code=True
        ).eval()
        
    def generate_response(self, history, temperature=1.0, top_p=1.0, top_k=50, max_length=1024):
    
        prompt = self.tokenizer.apply_chat_template(conversation=history, add_generation_prompt=True, tokenize=False)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs.to(self.model.device)
        with torch.no_grad():
            res = self.model.generate(**inputs, 
                                      max_new_tokens=max_length,
                                      temperature=temperature,
                                      top_k=top_k,
                                      top_p=top_p
                                      )
        responses = self.tokenizer.decode(res[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        response = responses.strip()
        return response
