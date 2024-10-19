from pydantic import BaseModel
from nonebot import get_driver, get_plugin_config


class ScopedConfig(BaseModel):
    default_context: int = 100
    prompt: str = (
        "你是一个总结聊天记录的专家，接下来你要把下面的聊天记录总结为几个重要事件，并按事件出现顺序排序，每个事件用一句话描述，这句话内要包括聊天的人都干了什么。全部内容不能超过300字。"
    )
    token: str
    base_url: str = "https://api.gpt.ge/v1/chat/completions"
    model_name: str = "gpt-4o-mini"


class Config(BaseModel):
    summary: ScopedConfig


global_config = get_driver().config
plugin_config = get_plugin_config(Config).summary
