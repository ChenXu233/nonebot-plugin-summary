from pydantic import BaseModel
from nonebot import get_driver, get_plugin_config
from nonebot.log import logger


class ScopedConfig(BaseModel):
    default_context: int = 300
    prompt: str = (
        """你是一个专业的文本总结员。你的主要任务是从聊天记录中提取关键信息，不包含任何其他多余的信息或解释。
能力:
从长段落中识别并提取关键信息。
把聊天记录总结为几个重要事件，并按事件出现顺序排序。请你判断哪些聊天是有关联的，将它们总结到一个事件，优先考虑讨论最多的话题。至少包含8个事件，每个事件用一段话详细描述，至少30字，这句话内要包括参与聊天的所有人都讨论了什么。将提取的信息准确地总结为一段结构清晰的文本。
在总结中标明事件的日期和大致时间（如早上、中午、下午、晚上、半夜），并包含时间，比如2024年10月16日上午8:46。
指南:
阅读聊天记录时，首先阅读并理解其中的内容。确定主题，找出关键信息。在总结单个事件时，只包含关键信息，尽量减少非主要信息的出现。总结的文本要简洁明了，避免任何可能引起混淆的复杂语句。
完成总结后，立即向用户提供，不需要询问用户是否满意或是否需要进一步的修改和优化。
严格按照以下输出格式：
markdown列表，每一个事件为一项，格式要求如下
1. （事件标题）xxxx年xx月xx日晚上xx:xx，讨论了什么，讨论了多久
...
"""
    )
    url_prompt:str = """你是一个专业的html文件总结员，请你总结以下html中的信息。"""
    token: str
    base_url: str = "https://api.gpt.ge/v1"
    model_name: str = "gpt-4o-mini"
    timezone: str = "Asia/Shanghai"
    aggregate_message:bool = True

    class Config:
        protected_namespaces = ()

class Config(BaseModel):
    summary: ScopedConfig


global_config = get_driver().config
plugin_config = get_plugin_config(Config).summary

logger.info(plugin_config.model_dump_json())