import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def main():
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    print(f"Loading {model_id}...")
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(model_id)
    mod = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, low_cpu_mem_usage=True)
    mod.eval()
    print("Load time:", round(time.time() - t0, 2), "s")
    
    prompt = "Who owns Project Atlas and why is it blocked?"
    inputs = tok(prompt, return_tensors="pt")
    
    t1 = time.time()
    with torch.inference_mode():
        out = mod.generate(**inputs, max_new_tokens=80, do_sample=False)
    gen_time = time.time() - t1
    print("Inference time:", round(gen_time, 2), "s")
    print("Speed:", round(80 / gen_time, 2), "tokens/sec")
    print("\nGenerated:\n", tok.decode(out[0], skip_special_tokens=True))

if __name__ == "__main__":
    main()
