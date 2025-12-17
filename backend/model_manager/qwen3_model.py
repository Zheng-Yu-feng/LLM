
from transformers import AutoModelForCausalLM, AutoTokenizer
from .base_model import ChatModel
import torch

class QwenModel(ChatModel):
    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained("qwen", trust_remote_code=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            "qwen", torch_dtype="auto", device_map="auto"
        ).eval()

    def generate_response(self, history, temperature=1.0, top_p=1.0, top_k=50, max_length=1024):
        input_ids = self.tokenizer.apply_chat_template(history, tokenize=False, add_generation_prompt=True)
        # print(f"qwen input_ids:{input_ids}")
        model_inputs = self.tokenizer([input_ids], return_tensors="pt", padding=True, truncation=True).to(self.model.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                model_inputs.input_ids,
                max_new_tokens=max_length,
                attention_mask=model_inputs.attention_mask,
                do_sample=True,
                temperature = temperature,
                top_p = top_p,
                top_k = top_k
            )
        generated_ids = [
            output_ids[len(model_inputs.input_ids[0]):] for output_ids in generated_ids
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0] 
        return response
