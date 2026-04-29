import argparse
from pathlib import Path

from transformers import AutoTokenizer
from peft import PeftModel
from transformers import AutoModelForCausalLM

from config import BASE_MODEL_NAME, FINAL_MODEL_DIR, TRAINED_MODEL_DIR


def latest_checkpoint(path):
    checkpoints = [
        child for child in Path(path).glob("checkpoint-*")
        if child.is_dir() and child.name.split("-")[-1].isdigit()
    ]
    if not checkpoints:
        return Path(path)
    return max(checkpoints, key=lambda child: int(child.name.split("-")[-1]))


def main():
    parser = argparse.ArgumentParser(description="Save a trained LoRA checkpoint as the final model adapter.")
    parser.add_argument("--checkpoint", default=None, help="Checkpoint directory. Defaults to latest checkpoint.")
    parser.add_argument("--output-dir", default=str(FINAL_MODEL_DIR), help="Final adapter output directory.")
    args = parser.parse_args()

    checkpoint_path = Path(args.checkpoint) if args.checkpoint else latest_checkpoint(TRAINED_MODEL_DIR)

    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME)
    model = PeftModel.from_pretrained(base_model, checkpoint_path)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

    output_dir = Path(args.output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print(f"Done. Final Model saved to {output_dir} from {checkpoint_path}")


if __name__ == "__main__":
    main()
