from transformers import AutoTokenizer
from peft import PeftModel
from transformers import AutoModelForCausalLM

#update checkpoint and model
checkpoint_path = "models/trained_model/checkpoint-700"
final_model_path = "models/final_model/final_model_v5"
base_model_name = "Qwen/Qwen2-0.5B"

base_model = AutoModelForCausalLM.from_pretrained(base_model_name)

model = PeftModel.from_pretrained(base_model, checkpoint_path)

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

model.save_pretrained(final_model_path)
tokenizer.save_pretrained(final_model_path)

print(f"Done. Final Model saved to {final_model_path}")