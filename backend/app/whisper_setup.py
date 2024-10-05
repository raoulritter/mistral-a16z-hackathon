import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

def setup_whisper():
    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device != "cpu" else torch.float32

    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-large-v3-turbo",
        torch_dtype=torch_dtype,
        device=device,
        # model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
    )

    return pipe

def transcribe_audio(pipe, audio):
    result = pipe(
        audio,
        chunk_length_s=30,
        batch_size=24,
        return_timestamps=True,
    )
    return result["text"], result["chunks"]