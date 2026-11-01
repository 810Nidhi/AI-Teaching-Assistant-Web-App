import config 
from huggingface_hub import InferenceClient
MODELS=getattr(config,"HF_MODELS",["meta-llama/Llama-3.1-8B"])
def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    key=getattr(config,"HF_API_KEY",None)
    if not key:
        return "Hf_API _KEY is missing in config.py"
    last_err=None
    for m in MODELS:
        try:
            c=InferenceClient(model=m,token=key)
            r = c.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content or ""
        except Exception as e:
            last_err=e
    return(
        "HF MODEL failed\n"
        f"Tried Models:{MODELS}\n"
        "Fix\n"
        "1)Switch to groq by importing groq.py in main.py"
        "2)Replace HF model in hf.py\n"
        f"Details:{type(last_err).__name__}:{last_err}")