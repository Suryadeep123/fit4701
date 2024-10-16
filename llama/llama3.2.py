import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

# Load the model and tokenizer
model_name = "meta-llama/Llama-3.2-1B"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# Example input text
input_text = "Once upon a time"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate output
with torch.no_grad():
    outputs = model.generate(**inputs)

# Decode and print the output
print(tokenizer.decode(outputs[0], skip_special_tokens=True))