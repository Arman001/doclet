import os
from huggingface_hub import hf_hub_download

MODELS_DIR = "models"
REPO_ID = "bartowski/Llama-3.2-1B-Instruct-GGUF"
FILENAME = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"

def download_model():
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
    
    print(f"Downloading {FILENAME} from {REPO_ID}...")
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        local_dir=MODELS_DIR,
        local_dir_use_symlinks=False
    )
    print(f"Model downloaded to: {model_path}")

if __name__ == "__main__":
    download_model()
