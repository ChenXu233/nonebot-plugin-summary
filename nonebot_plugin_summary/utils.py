import abc
import inspect
import httpx

from typing import List
from sqlalchemy import or_, select

from nonebot_plugin_chatrecorder.model import MessageRecord
from nonebot_plugin_orm import get_session
from nonebot_plugin_userinfo import get_user_info
from nonebot_plugin_session_orm import get_session_by_persist_id, SessionModel
from nonebot_plugin_session import Session

from .config import plugin_config


__usage__ = inspect.cleandoc(
    """
总结群聊消息

使用方法：
/省流 -q [int] -g [str] -n [int] -t [gap-time-str]

/省流 --直接调用，默认爬100楼
/省流 200 --爬取200楼
/省流 -n 200 --同上
/省流 -i 114514 --爬取id114514在本群的发言
/省流 -g 100000 -- 爬取群号100000的发言
/省流 -t 2024-01-01-2024-01-14 --爬取2024-01-01至2024-01-14的发言

"""
)


class BaseLLMModel(abc.ABC):
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.http_client = httpx.AsyncClient()

    @abc.abstractmethod
    async def post_content(self, prompt: str, string: str) -> str:
        raise NotImplementedError

    async def summary(self, string: str) -> str:
        return await self.post_content(self.prompt, string)

    async def set_prompt(self, prompt: str) -> None:
        self.prompt = prompt


class OpenAIModel(BaseLLMModel):
    def __init__(self, prompt: str, api_key: str, model_name: str, endpoint: str):
        super().__init__(prompt)
        self.model_name = model_name
        self.api_key = api_key
        self.endpoint = endpoint

    async def post_content(self, prompt: str, string: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": string},
            ],
            "max_tokens": 1688,
            "temperature": 0.5,
            "stream": False,
        }
        data = await self.http_client.post(self.endpoint, headers=headers, json=data)
        print(data.json())
        return data.json()["choices"][0]["message"]["content"]


models = {"OpenAI": OpenAIModel}


async def build_records(bot, event, records: List[MessageRecord]) -> str:
    s = ""
    for i in records:
        session = await get_session_by_persist_id(i.session_persist_id)
        user_id = session.id1
        if not user_id:
            continue
        user_info = await get_user_info(bot, event, user_id)
        if not user_info:
            continue
        name = (
            user_info.user_displayname
            if user_info.user_displayname
            else user_info.user_name if user_info.user_name else user_info.user_id
        )
        msg = i.plain_text
        s += f"{name}:{msg}\n"
    return s


async def get_records(
    session: Session, number: int = plugin_config.default_context
) -> List[MessageRecord]:
    where = [
        or_(SessionModel.id2 == session.id2),
        or_(SessionModel.id == MessageRecord.session_persist_id),
    ]
    statement = select(MessageRecord).where(*where)
    async with get_session() as db_session:
        records = [i for i in ((await db_session.scalars(statement)).all())[-number:]]

    return records
