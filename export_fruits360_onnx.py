import torch
import torchvision.models as models
from huggingface_hub import hf_hub_download
import json

REPO_ID = "bhumong/fruit-classifier-efficientnet-b0"
ONNX_OUTPUT = "fruit_classifier.onnx"
LABELS_OUTPUT = "fruit_labels.txt"
IMG_SIZE = 224  # EfficientNet-B0 input size

def main():
    # Load config for label mapping
    config_path = hf_hub_download(repo_id=REPO_ID, filename="config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    num_labels = config["num_labels"]
    id2label = {int(k): v for k, v in config["id2label"].items()}

    # Build model
    model = models.efficientnet_b0(weights=None)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(num_ftrs, num_labels)

    # Load weights
    weights_path = hf_hub_download(repo_id=REPO_ID, filename="pytorch_model.bin")
    state_dict = torch.load(weights_path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    # Dummy input for ONNX export
    dummy = torch.randn(1, 3, IMG_SIZE, IMG_SIZE, dtype=torch.float32)

    # Export
    torch.onnx.export(
        model,
        dummy,
        ONNX_OUTPUT,
        input_names=["input"],
        output_names=["logits"],
        dynamic_axes={"input": {0: "batch"}, "logits": {0: "batch"}},
        opset_version=13,
    )

    print(f"SAVED ONNX → {ONNX_OUTPUT}")

    # Save labels
    with open(LABELS_OUTPUT, "w") as f:
        for i in range(num_labels):
            f.write(id2label[i] + "\n")

    print(f"SAVED LABELS → {LABELS_OUTPUT}")
    print("DONE.")

if __name__ == "__main__":
    main()
