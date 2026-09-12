from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Buttons:
    """ ? Создание кнопок для выбора модели: """
    
    @staticmethod
    def get_setmodel_inline_kb() -> InlineKeyboardButton:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="DeepSeek-R1", callback_data="deepseek-ai/DeepSeek-R1")],
        [InlineKeyboardButton(text="DeepSeek-R1-Llama-70B", callback_data="deepseek-ai/DeepSeek-R1-Distill-Llama-70B",)],
        [InlineKeyboardButton(text="DeepSeek-R1-Qwen-32B", callback_data="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")],
        [InlineKeyboardButton(text="Qwen/Qwen3-235B-A22B-FP8", callback_data="Qwen/Qwen3-235B-A22B-FP8")],
        [InlineKeyboardButton(text="Qwen/QwQ-32B", callback_data="Qwen/QwQ-32B")],
        [InlineKeyboardButton(text="Qwen2.5-Coder-32B", callback_data="Qwen/Qwen2.5-Coder-32B-Instruct")],
        [InlineKeyboardButton(text="Qwen/Qwen2.5-1.5B-Instruct", callback_data="Qwen/Qwen2.5-1.5B-Instruct")],
        [InlineKeyboardButton(text="ozone-ai", callback_data="ozone-ai/0x-lite")],
        [InlineKeyboardButton(text="google/gemma-3-27b-it", callback_data="google/gemma-3-27b-it")],
        [InlineKeyboardButton(text="Mistral-Large-2411", callback_data="mistralai/Mistral-Large-Instruct-2411")],
        [InlineKeyboardButton(text="Ministral-8B-2410", callback_data="mistralai/Ministral-8B-Instruct-2410")],
        [InlineKeyboardButton(text="microsoft/Phi-3.5", callback_data="microsoft/Phi-3.5-mini-instruct")],
        [InlineKeyboardButton(text="microsoft/phi-4", callback_data="microsoft/phi-4")],
        [InlineKeyboardButton(text="meta-Llama-3.3-70B", callback_data="meta-llama/Llama-3.3-70B-Instruct")],
        [InlineKeyboardButton(text="Llama-3.1-Nemotron-70B", callback_data="neuralmagic/Llama-3.1-Nemotron-70B-Instruct-HF-FP8-dynamic")],
        [InlineKeyboardButton(text="Llama-4-Maverick-17B-128E-Instruct-FP8", callback_data="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8")],
        [InlineKeyboardButton(text="SentientAGI/Dobby-Mini-Llama-3.1-8B", callback_data="SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B")],
        [InlineKeyboardButton(text="nvidia/AceMath-7B", callback_data="nvidia/AceMath-7B-Instruct")],
        [InlineKeyboardButton(text="databricks/dbrx-instruct", callback_data="databricks/dbrx-instruct")],
        [InlineKeyboardButton(text="Confucius-o1-14B", callback_data="netease-youdao/Confucius-o1-14B")],
        [InlineKeyboardButton(text="watt-tool-70B", callback_data="watt-ai/watt-tool-70B")],
        [InlineKeyboardButton(text="Bespoke-Stratos-32B", callback_data="bespokelabs/Bespoke-Stratos-32B")],
        [InlineKeyboardButton(text="Sky-T1-32B", callback_data="NovaSky-AI/Sky-T1-32B-Preview")],
        [InlineKeyboardButton(text="Falcon3-10B", callback_data="tiiuae/Falcon3-10B-Instruct")],
        [InlineKeyboardButton(text="CohereForAI", callback_data="CohereForAI/c4ai-command-r-plus-08-2024")],
        [InlineKeyboardButton(text="THUDM/glm-4-9b-chat", callback_data="THUDM/glm-4-9b-chat")],
        [InlineKeyboardButton(text="CohereForAI/aya-expanse-32b", callback_data="CohereForAI/aya-expanse-32b")],
        [InlineKeyboardButton(text="jinaai/ReaderLM-v2", callback_data="jinaai/ReaderLM-v2")],
        [InlineKeyboardButton(text="openbmb/MiniCPM3-4B", callback_data="openbmb/MiniCPM3-4B")],
        [InlineKeyboardButton(text="ibm-granite-3.1-8b", callback_data="ibm-granite/granite-3.1-8b-instruct")],
        [InlineKeyboardButton(text="❌ cancel ❌", callback_data="cancel")]
        ], resize_keyboard=True)
        return keyboard


    @staticmethod
    def get_setvismodel_inline_kb() -> InlineKeyboardButton:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Qwen2-VL-7B", callback_data="Qwen/Qwen2-VL-7B-Instruct")],
        [InlineKeyboardButton(text="Llama-3.2-90B-Vision", callback_data="meta-llama/Llama-3.2-90B-Vision-Instruct")],
        [InlineKeyboardButton(text="❌ cancel ❌", callback_data="cancel")]
        ], resize_keyboard=True)
        return keyboard