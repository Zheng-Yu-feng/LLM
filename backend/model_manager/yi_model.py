from transformers import AutoModelForCausalLM, AutoTokenizer
from .base_model import ChatModel
import torch

class YiModel(ChatModel):
    def load(self):
        model_path = 'Yi'
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        # Since transformers 4.35.0, the GPT-Q/AWQ model can be loaded using AutoModelForCausalLM.
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype='auto'
        ).eval()

    def generate_response(self, history, temperature=1.0, top_p=1.0, top_k=50, max_length=1024):
        input_ids = self.tokenizer.apply_chat_template(conversation=history, tokenize=True, return_tensors='pt')
        #print(f"Yi input_ids:{input_ids}")
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids.to(self.model.device), 
                eos_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=max_length,
                temperature = temperature,
                top_p = top_p,
                top_k = top_k
                
                )
        response = self.tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
        
        return response
