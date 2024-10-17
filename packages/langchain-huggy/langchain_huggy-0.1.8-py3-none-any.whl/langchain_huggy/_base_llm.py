from typing import List

from hugchat.hugchat import ChatBot

from ._base_login import HFCredentialManager
from .const import AVAILABLE_MODEL_LIST
class BaseHuggyLLM(HFCredentialManager, ChatBot):
    MODELS: List[str] = AVAILABLE_MODEL_LIST

    def __new__(cls, hf_email=None, hf_password=None, cookie_dir_path="./cookies/", save_cookies=True,
                system_prompt:str = "",default_llm:int = 3):
        instance = super().__new__(cls)
        instance.__init__(hf_email, hf_password, cookie_dir_path, save_cookies)
        return ChatBot(default_llm=default_llm,system_prompt=system_prompt,cookies=instance.cookies.get_dict())
