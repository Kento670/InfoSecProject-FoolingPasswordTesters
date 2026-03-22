from transformers import AutoTokenizer
from peft import PeftModel
from transformers import AutoModelForCausalLM

CHECKPOINT_PATH = "models/trained_model/checkpoint-300"
FINAL_MODEL_PATH = "models/final_model"
BASE_MODEL_NAME = "Qwen/Qwen2-0.5B"

base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME)

model = PeftModel.from_pretrained(base_model, CHECKPOINT_PATH)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

model.save_pretrained(FINAL_MODEL_PATH)
tokenizer.save_pretrained(FINAL_MODEL_PATH)

print(f"Final Model saved to {FINAL_MODEL_PATH}")