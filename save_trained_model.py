import argparse

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    parser = argparse.ArgumentParser(description="Save a trained LoRA checkpoint for inference.")
    parser.add_argument("--checkpoint", default="models/trained_model/checkpoint-800")
    parser.add_argument("--output", default="models/final_model/final_model_v4")
    parser.add_argument("--base-model", default="Qwen/Qwen2-0.5B")
    args = parser.parse_args()

    base_model = AutoModelForCausalLM.from_pretrained(args.base_model)
    model = PeftModel.from_pretrained(base_model, args.checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)

    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)

    print(f"Done. Final model saved to {args.output}")


if __name__ == "__main__":
    main()
