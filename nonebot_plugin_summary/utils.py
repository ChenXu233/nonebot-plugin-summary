import abc
import inspect

from datetime import datetime
from tzlocal import get_localzone
from openai import AsyncOpenAI
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

    @abc.abstractmethod
    async def post_content(self, string: str) -> str:
        raise NotImplementedError

    async def summary(self, string: str) -> str:
        try:
            return await self.post_content(string)
        except Exception as e:
            return f"请求错误\n{e}"

    async def set_prompt(self, prompt: str) -> None:
        self.prompt = prompt


class OpenAIModel(BaseLLMModel):
    def __init__(self, prompt: str, api_key: str, model_name: str, endpoint: str):
        super().__init__(prompt)
        self.model_name = model_name
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = AsyncOpenAI(api_key=api_key, base_url=endpoint,timeout=60)

    async def post_content(self, string: str) -> str:
        completion = await self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.prompt},

                {"role": "user", "content": string}
            ],
        )
        if not completion.choices[0].message.content:
            return "生产内容错误，请检查模型是否可用"
        return completion.choices[0].message.content


models = {"OpenAI": OpenAIModel}

async def build_records(bot, event, records: List[MessageRecord]) -> str:
    s = ""
    local_tz = get_localzone()
    local_now = datetime.now(local_tz)
    offset = local_now.utcoffset()  # Returns a timedelta

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
        s += f"\"{name}\"在{(i.time + offset).replace(tzinfo=local_tz).strftime('%Y-%m-%d %H:%M:%S')}说:{msg}\n" # type: ignore
    s+="\n\n现在的时间是"+ datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return s


async def get_records(
    session: Session,
    number: int = plugin_config.default_context
) -> List[MessageRecord]:
    where = [
        or_(SessionModel.id2 == session.id2),
        or_(SessionModel.id == MessageRecord.session_persist_id),
    ]
    statement = select(MessageRecord).where(*where)
    async with get_session() as db_session:
        records = [i for i in ((await db_session.scalars(statement)).all())[-number:]]

    return records
