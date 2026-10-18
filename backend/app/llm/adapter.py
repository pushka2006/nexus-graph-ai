import logging
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.config import get_settings

logger = logging.getLogger("nexus.llm.adapter")


class LLMAdapter:
    """
    Production-grade AI Model Adapter supporting:
    1. Local Hugging Face Transformers (e.g. Qwen/Qwen2.5-3B-Instruct or Qwen2.5-0.5B)
    2. OpenAI-compatible remote endpoints (OpenAI, vLLM, Ollama, LiteLLM)
    3. Explicit diagnostics, latency telemetry, memory monitoring, and health checking.
    """
    def __init__(self):
        self.settings = get_settings()
        self.provider = self.settings.LLM_PROVIDER.lower()
        self.model_name = self.settings.MODEL_NAME
        self.hf_device = self.settings.HF_DEVICE
        self._hf_pipeline = None
        self._tokenizer = None
        self._model = None
        self._is_loaded = False
        self._load_error = None
        self._last_health_check = None

    def _lazy_load_hf(self):
        """Loads the configured Hugging Face model and tokenizer on configured device."""
        if self._is_loaded:
            return

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

            logger.info(f"Loading Hugging Face model {self.model_name} on {self.hf_device}...")
            start_load = time.time()
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Detect device capabilities
            use_device = "cuda" if torch.cuda.is_available() and self.hf_device != "cpu" else "cpu"
            dtype = getattr(torch, self.settings.TORCH_DTYPE, torch.float32)

            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                dtype=dtype,
                device_map="auto" if use_device == "cuda" else None,
                low_cpu_mem_usage=False
            )
            if use_device == "cpu":
                self._model = self._model.to("cpu")
            self._model.eval()

            self._hf_pipeline = pipeline(
                "text-generation",
                model=self._model,
                tokenizer=self._tokenizer
            )
            self._is_loaded = True
            self._load_error = None
            logger.info(f"Loaded {self.model_name} in {round(time.time() - start_load, 2)}s.")
        except Exception as e:
            self._is_loaded = False
            self._load_error = f"Failed to load Hugging Face model '{self.model_name}': {str(e)}"
            logger.error(self._load_error)
            raise RuntimeError(self._load_error)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 120,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes real inference through the configured provider.
        Never silently switches to mock mode if a real provider fails.
        """
        start_time = time.time()

        # Format grounded FalkorDB facts into context block
        context_block = ""
        if context_data:
            direct_facts = context_data.get("direct_facts", [])
            evidence_paths = context_data.get("evidence_paths", [])
            conflicts = context_data.get("conflicting_evidence", [])
            parts = []
            if direct_facts:
                parts.append("VERIFIED FALKORDB FACTS:\n" + "\n".join(f"- {f}" for f in direct_facts[:6]))
            if evidence_paths:
                parts.append("GRAPH RELATIONSHIPS:\n" + "\n".join(f"- {p}" for p in evidence_paths[:4]))
            if conflicts:
                parts.append("DOCUMENT CONFLICTS:\n" + "\n".join(f"- {c}" for c in conflicts[:2]))
            if parts:
                context_block = "\n\n" + "\n\n".join(parts)

        # 1. Hugging Face Local Transformers
        if self.provider == "huggingface":
            self._lazy_load_hf()
            if not self._hf_pipeline:
                raise RuntimeError(f"Hugging Face pipeline is not available: {self._load_error}")

            user_content = f"{prompt}{context_block}\n\nSynthesize the exact answer grounded in the verified graph evidence above:"
            full_prompt = (
                f"<|im_start|>system\n{system_prompt or 'You are NEXUS GRAPH AI, an authoritative enterprise intelligence agent.'}<|im_end|>\n"
                f"<|im_start|>user\n{user_content}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )
            try:
                import torch
                with torch.inference_mode():
                    outputs = self._hf_pipeline(
                        full_prompt,
                        max_new_tokens=min(max_tokens, 120),
                        do_sample=False,
                        return_full_text=False
                    )
                generated_text = outputs[0]["generated_text"].strip()
                latency_ms = round((time.time() - start_time) * 1000, 2)
                return {
                    "text": generated_text,
                    "model": self.model_name,
                    "provider": "huggingface",
                    "device": self.hf_device,
                    "latency_ms": latency_ms,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Hugging Face inference error: {e}")
                raise RuntimeError(f"Hugging Face inference failed on device {self.hf_device}: {str(e)}")

        # 2. OpenAI / vLLM / Ollama compatible remote API
        elif self.provider in ("openai", "vllm"):
            import httpx
            headers = {}
            if self.settings.OPENAI_API_KEY:
                headers["Authorization"] = f"Bearer {self.settings.OPENAI_API_KEY}"
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt or "You are NEXUS GRAPH AI enterprise intelligence agent."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            try:
                endpoint = f"{self.settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions"
                resp = httpx.post(endpoint, headers=headers, json=payload, timeout=45.0)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    latency_ms = round((time.time() - start_time) * 1000, 2)
                    return {
                        "text": content,
                        "model": data.get("model", self.model_name),
                        "provider": self.provider,
                        "endpoint": endpoint,
                        "latency_ms": latency_ms,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    err_msg = f"Remote inference endpoint returned HTTP {resp.status_code}: {resp.text}"
                    logger.error(err_msg)
                    raise RuntimeError(err_msg)
            except Exception as e:
                logger.error(f"Remote LLM request error: {e}")
                raise RuntimeError(f"Remote LLM inference failed on {self.settings.OPENAI_BASE_URL}: {str(e)}")

        # 3. Explicit Mock Provider (Only when LLM_PROVIDER is explicitly configured as 'mock')
        elif self.provider == "mock":
            return self._domain_grounded_mock(prompt, context_data, start_time)

        else:
            raise ValueError(f"Unsupported LLM_PROVIDER '{self.provider}'. Must be 'huggingface', 'openai', 'vllm', or 'mock'.")

    def health_check(self) -> Dict[str, Any]:
        """
        Performs an inexpensive check to verify if the configured provider and model
        are truly operational.
        """
        start_t = time.time()
        self._last_health_check = datetime.utcnow().isoformat()

        if self.provider == "huggingface":
            try:
                import torch
                import transformers
                cuda_ok = torch.cuda.is_available()
                return {
                    "status": "ready" if self._is_loaded else "standby",
                    "provider": "huggingface",
                    "model_id": self.model_name,
                    "device": self.hf_device,
                    "cuda_available": cuda_ok,
                    "torch_version": torch.__version__,
                    "transformers_version": transformers.__version__,
                    "is_loaded": self._is_loaded,
                    "load_error": self._load_error,
                    "latency_ms": round((time.time() - start_t) * 1000, 2),
                    "last_check": self._last_health_check
                }
            except ImportError as e:
                return {
                    "status": "unavailable",
                    "provider": "huggingface",
                    "model_id": self.model_name,
                    "device": self.hf_device,
                    "error": f"Required packages missing: {str(e)}",
                    "latency_ms": round((time.time() - start_t) * 1000, 2),
                    "last_check": self._last_health_check
                }

        elif self.provider in ("openai", "vllm"):
            import httpx
            headers = {}
            if self.settings.OPENAI_API_KEY:
                headers["Authorization"] = f"Bearer {self.settings.OPENAI_API_KEY}"
            endpoint = f"{self.settings.OPENAI_BASE_URL.rstrip('/')}/models"
            try:
                resp = httpx.get(endpoint, headers=headers, timeout=5.0)
                latency_ms = round((time.time() - start_t) * 1000, 2)
                if resp.status_code == 200:
                    return {
                        "status": "ready",
                        "provider": self.provider,
                        "model_id": self.model_name,
                        "endpoint": self.settings.OPENAI_BASE_URL,
                        "latency_ms": latency_ms,
                        "last_check": self._last_health_check
                    }
                else:
                    return {
                        "status": "error",
                        "provider": self.provider,
                        "model_id": self.model_name,
                        "endpoint": self.settings.OPENAI_BASE_URL,
                        "http_code": resp.status_code,
                        "error": resp.text[:200],
                        "latency_ms": latency_ms,
                        "last_check": self._last_health_check
                    }
            except Exception as e:
                return {
                    "status": "unavailable",
                    "provider": self.provider,
                    "model_id": self.model_name,
                    "endpoint": self.settings.OPENAI_BASE_URL,
                    "error": str(e),
                    "latency_ms": round((time.time() - start_t) * 1000, 2),
                    "last_check": self._last_health_check
                }

        elif self.provider == "mock":
            return {
                "status": "mock_mode_active",
                "provider": "mock",
                "model_id": f"{self.model_name} (Deterministic Mock)",
                "device": "cpu",
                "latency_ms": 1.5,
                "warning": "Mock provider active. Set LLM_PROVIDER to 'huggingface' or 'openai' for live model weights.",
                "last_check": self._last_health_check
            }

        return {
            "status": "unknown",
            "provider": self.provider,
            "error": f"Unknown provider '{self.provider}'",
            "last_check": self._last_health_check
        }

    def _domain_grounded_mock(self, prompt: str, context: Optional[Dict[str, Any]], start_time: float) -> Dict[str, Any]:
        """Explicit mock generator, labeled transparently."""
        p = prompt.lower()
        if "atlas" in p and ("own" in p or "block" in p or "prevent" in p or "release" in p):
            text = (
                "Project Atlas is owned by Maya Lin (Principal Product Manager, emp_11) and executive-sponsored by "
                "Elena Vance (Chief Product Officer, emp_02). The project is currently BLOCKED by Architecture Decision "
                "AD-104 ('Project Atlas Production Gate and Cloud Storage Migration'), which is pending formal security sign-off "
                "from VP Engineering Dr. Aris Thorne. AD-104 is held up because the proposed S3 cloud storage does not yet comply with "
                "the newly enacted Information Security Policy v2.0 (doc_sec_pol_v20), which superseded v1.2 and requires Customer-Managed "
                "KMS Keys (CMK) on all production data buckets."
            )
        elif "security" in p or "sec-014" in p or "sec_014" in p or "investigate" in p:
            text = (
                "Security investigation complete for event SEC-014 ('Abnormal Token Generation with Admin Privilege Escalation'): "
                "The anomaly originated from service worker svc-atlas-worker (IP 10.0.4.152). Multi-hop graph traversal connects SEC-014 directly to "
                "Ticket TIK-204 ('Unauthorized Internal Service Token Generation on Atlas Microservice') and active Incident INC-08. "
                "The affected subsystem is Project Atlas. The primary assigned responder is Zack Brody (emp_09, SecOps Incident Handler), "
                "under CISO Kaelen Voss. Containment recommendation: immediately revoke the compromised worker token and rotate Atlas IAM credentials."
            )
        elif "memory" in p or "previous" in p or "prior" in p or "recall" in p:
            text = (
                "Recovered episodic and semantic memories from shared agent storage: Prior investigation (mem_init_01) by Graph Reasoning Agent "
                "established that Project Atlas is blocked by AD-104 awaiting Elena Vance's sign-off. Procedural memory PB-SEC-01 outlines the "
                "authorized protocol for token containment."
            )
        elif "policy" in p or "supersede" in p or "conflict" in p:
            text = (
                "Graph conflict detected: Information Security Policy v2.0 (doc_sec_pol_v20) explicitly SUPERSEDES v1.2 (doc_sec_pol_v12). "
                "Policy v2.0 mandates strict AWS KMS customer-managed keys for all cloud storage buckets, creating a direct conflict with older legacy guidelines."
            )
        else:
            ctx_summary = f" (Context: {len(context)} records evaluated)" if context else ""
            text = (
                f"Based on authoritative FalkorDB graph traversal and company documentation{ctx_summary}, "
                f"the requested company intelligence query has been analyzed with grounded evidence."
            )

        return {
            "text": text,
            "model": f"{self.model_name} (Deterministic Mock)",
            "provider": "mock",
            "latency_ms": round((time.time() - start_time) * 1000 + 15.0, 2),
            "timestamp": datetime.utcnow().isoformat()
        }


_adapter_instance = None

def get_llm_adapter() -> LLMAdapter:
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = LLMAdapter()
    return _adapter_instance
