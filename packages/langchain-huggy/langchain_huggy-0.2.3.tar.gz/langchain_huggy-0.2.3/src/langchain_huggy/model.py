from typing import Any, Dict, List, Optional, Union, Iterator
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ChatMessage, HumanMessage, SystemMessage, BaseMessageChunk
from langchain_core.outputs import ChatGeneration, ChatResult, ChatGenerationChunk
from hugchat import hugchat
from hugchat.login import Login
from configparser import ConfigParser
import os

from langchain_core.runnables import RunnableConfig

DEFAULT_MODELS = ['meta-llama/Meta-Llama-3.1-70B-Instruct', 'CohereForAI/c4ai-command-r-plus-08-2024', 'Qwen/Qwen2.5-72B-Instruct', 'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF', 'meta-llama/Llama-3.2-11B-Vision-Instruct', 'NousResearch/Hermes-3-Llama-3.1-8B', 'mistralai/Mistral-Nemo-Instruct-2407', 'microsoft/Phi-3.5-mini-instruct']



class HuggingChat(BaseChatModel):
    cookies: Dict[str, str] = None
    chatbot: hugchat.ChatBot = None
    model:str = DEFAULT_MODELS[2]
    hf_email: Optional[str] = None
    hf_password: Optional[str] = None
    system_prompt: Optional[str] = None



    def __init__(self, model: str = None,system_prompt = "",**kwargs):
        super().__init__(**kwargs)
        self.model = model or self.model
        self.system_prompt = system_prompt
        self._authorize()
        self.cookies = self._setup_login()
        self.chatbot = self._setup_chatbot()

    @property
    def _llm_type(self) -> str:
        return "hugging-chat"

    @property
    def get_available_models(self):
        return DEFAULT_MODELS


    def _authorize(self):
        if self.hf_email is None:
            self.hf_email = os.getenv("HUGGINGFACE_EMAIL")
            if not self.hf_email:
                raise ValueError("env HUGGINGFACE_EMAIL or pass hf_email are required to login.")
        if self.hf_password is None:
            self.hf_password = os.getenv("HUGGINGFACE_PASSWD")
            if not self.hf_password:
                raise ValueError("env HUGGINGFACE_PASSWD or pass hf_password are required to login.")


    def _setup_login(self) -> Dict[str, str]:
        cookie_path_dir = "./cookies/"
        sign = Login(self.hf_email, self.hf_password)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        return cookies.get_dict()

    def _setup_chatbot(self) -> hugchat.ChatBot:
        return hugchat.ChatBot(cookies=self.cookies, default_llm=self.model,
                               system_prompt=self.system_prompt)

    def _convert_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        prompt = ""

        if isinstance(messages,str):
            return messages
        elif isinstance(messages,list) and isinstance(messages[0],list) and isinstance(messages[0][0],HumanMessage):
            messages = messages[0]

        for message in messages:
            if isinstance(message, SystemMessage):
                prompt += f"System: {message.content}\n"
            elif isinstance(message, HumanMessage):
                prompt += f"Human: {message.content}\n"
            elif isinstance(message, AIMessage):
                prompt += f"AI: {message.content}\n"
            elif isinstance(message, ChatMessage):
                prompt += f"{message.role.capitalize()}: {message.content}\n"
        return prompt.strip()

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        prompt = self._convert_messages_to_prompt(messages)
        response = self.chatbot.chat(prompt, **kwargs)
        ai_message = AIMessage(content=response.text)
        chat_generation = ChatGeneration(message=ai_message)
        return ChatResult(generations=[chat_generation])

    def _add_system_prompt(self, query: str) -> str:
        system_prompt = """
        You are an AI assistant created by OmniAI. Approach each query with careful consideration and analytical thinking. When responding:

        1. Thoroughly analyze complex and open-ended questions, but be concise for simpler tasks.
        2. Break down problems systematically before providing final answers.
        3. Engage in discussions on a wide variety of topics with intellectual curiosity.
        4. For long tasks that can't be completed in one response, offer to do them piecemeal and get user feedback.
        5. Use markdown for code formatting.
        6. Avoid unnecessary affirmations or filler phrases at the start of responses.
        7. Respond in the same language as the user's query.
        8. Do not apologize if you cannot or will not perform a task; simply state that you cannot do it.
        9. If asked about very obscure topics, remind the user at the end that you may hallucinate in such cases.
        10. If citing sources, inform the user that you don't have access to a current database and they should verify any citations.
        """
        return system_prompt

    def generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        return self._generate(messages, stop, run_manager, **kwargs)

    def stream(
            self,
            input: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> Iterator[BaseMessageChunk]:
        if isinstance(input,list):
            self.chatbot.new_conversation(system_prompt=input[0]["content"],switch_to=True)
            input = input[1]["content"] # query
        prompt = self._convert_messages_to_prompt(input)
        for resp in self.chatbot.chat(prompt, stream=True, **kwargs):
            if resp and isinstance(resp, dict) and 'token' in resp:
                chunk = AIMessage(content=resp['token'])
                yield chunk

    def pstream(self, messages):
        for x in self.stream(messages):
            if isinstance(x, BaseMessage):
                print(x.content, end="", flush=True)

    def invoke(
        self,
        input: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> BaseMessage:
        if isinstance(input,list):
            self.chatbot.new_conversation(system_prompt=input[0]["content"],switch_to=True)
            input = input[1]["content"] # query
        prompt = self._convert_messages_to_prompt(input)
        response = self.chatbot.chat(prompt, **kwargs)
        response = response.wait_until_done()
        return AIMessage(content=response)

