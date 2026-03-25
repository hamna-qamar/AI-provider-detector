"""
AI Provider Detector
====================
A Python utility that detects the AI model provider based on model string prefix.
This is the core logic needed for Sugar-AI's Issue #51 implementation.

Supported Providers:
- HuggingFace (default Sugar-AI provider)
- OpenAI (gpt-3.5-turbo, gpt-4, etc.)
- Anthropic (claude-3, claude-2, etc.)
- Ollama (local models: llama2, mistral, etc.)

Author: Hamna Qamar
GitHub: github.com/hamna-qamar
"""


class AIProviderDetector:
    """
    Detects AI model provider from model string prefix.
    Inspired by Sugar-AI Issue #51:
    github.com/sugarlabs/sugar-ai/issues/51
    """

    # Provider prefixes for detection
    PROVIDER_PREFIXES = {
        "openai":    ["gpt-3", "gpt-4", "gpt-o", "text-davinci"],
        "anthropic": ["claude-"],
        "ollama":    ["llama", "mistral", "gemma", "phi", "deepseek", "qwen"],
    }

    def detect_provider(self, model: str) -> str:
        """
        Detect provider from model string.

        Args:
            model (str): Model name e.g. 'gpt-4', 'claude-3', 'llama2'

        Returns:
            str: Provider name — 'openai', 'anthropic', 'ollama', or 'huggingface'
        """
        model_lower = model.lower().strip()

        for provider, prefixes in self.PROVIDER_PREFIXES.items():
            for prefix in prefixes:
                if model_lower.startswith(prefix):
                    return provider

        # Default to HuggingFace (existing Sugar-AI behavior)
        return "huggingface"

    def get_provider_info(self, model: str) -> dict:
        """
        Get full provider information for a given model.

        Args:
            model (str): Model name

        Returns:
            dict: Provider details including name, type, and setup info
        """
        provider = self.detect_provider(model)

        info = {
            "model": model,
            "provider": provider,
            "details": self._get_details(provider)
        }
        return info

    def _get_details(self, provider: str) -> dict:
        """Return setup details for each provider."""
        details = {
            "openai": {
                "type": "Cloud API",
                "requires": "OPENAI_API_KEY environment variable",
                "cost": "Paid — per token billing",
                "offline": False
            },
            "anthropic": {
                "type": "Cloud API",
                "requires": "ANTHROPIC_API_KEY environment variable",
                "cost": "Paid — per token billing",
                "offline": False
            },
            "ollama": {
                "type": "Local Model",
                "requires": "Ollama installed locally (ollama.ai)",
                "cost": "Free — runs on your own machine",
                "offline": True
            },
            "huggingface": {
                "type": "Cloud API (default)",
                "requires": "HuggingFace API key + AWS hosting",
                "cost": "Paid — cloud hosting required",
                "offline": False
            },
        }
        return details.get(provider, {})


def main():
    """
    Demo: Test the AI Provider Detector with various model strings.
    This simulates how Sugar-AI will detect providers after Issue #51 is resolved.
    """
    detector = AIProviderDetector()

    # Test models
    test_models = [
        "gpt-4",
        "gpt-3.5-turbo",
        "claude-3-opus",
        "claude-2",
        "llama2",
        "mistral",
        "gemma:7b",
        "deepseek-r1",
        "HuggingFaceH4/zephyr-7b-beta",
    ]

    print("=" * 55)
    print("   AI Provider Detector — Sugar-AI Issue #51 Demo")
    print("=" * 55)
    print(f"{'Model':<30} {'Provider':<15} {'Offline?'}")
    print("-" * 55)

    for model in test_models:
        info = detector.get_provider_info(model)
        offline = "Yes ✓" if info["details"].get("offline") else "No"
        print(f"{model:<30} {info['provider']:<15} {offline}")

    print("=" * 55)
    print("\nThis detection logic will be added to RAGAgent")
    print("in app/ai.py inside __init__ and set_model methods.")
    print("Reference: github.com/sugarlabs/sugar-ai/issues/51")


if __name__ == "__main__":
    main()
