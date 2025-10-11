# models/mistral_model.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class MistralAssistant:
    def __init__(self):
        print("🔹 Loading Mistral 7B model...")
        model_name = "mistralai/Mistral-7B-Instruct-v0.2"  # or your downloaded version
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=250,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )

    def get_response(self, prompt):
        system_prompt = (
            "You are a helpful AI assistant that provides clear, natural, and concise responses. "
            "If the user asks to perform a specific action like open apps, play music, or show weather, "
            "respond appropriately as a virtual assistant."
        )
        input_text = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        outputs = self.generator(input_text, do_sample=True)
        return outputs[0]["generated_text"].split("Assistant:")[-1].strip()
