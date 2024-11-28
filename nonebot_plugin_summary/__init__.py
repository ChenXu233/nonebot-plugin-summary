import re
import httpx
from nonebot import require

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
require("nonebot_plugin_chatrecorder")
require("nonebot_plugin_userinfo")
require("nonebot_plugin_session")
require("nonebot_plugin_session_orm")
require("nonebot_plugin_orm")
import nonebot_plugin_saa as saa
from nonebot_plugin_alconna import Alconna, Args, Option, on_alconna, Match, MsgId
from nonebot_plugin_alconna.builtins.extensions import ReplyRecordExtension
from nonebot_plugin_session import Session, extract_session
from nonebot_plugin_chatrecorder import get_message_records

from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.adapters import Bot, Event
from nonebot.params import Depends

from .utils import __usage__, build_records, OpenAIModel
from .time import get_datetime_fromisoformat_with_timezone, get_datetime_now_with_timezone
from .config import Config, plugin_config

__plugin_meta__ = PluginMetadata(
    name="省流",
    description="总结群友怪话",
    usage=__usage__,
    homepage="https://github.com/ChenXu233/nonebot-plugin-summary",
    type="application",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_chatrecorder", "nonebot_plugin_saa", "nonebot_plugin_alconna"
    ),
    config=Config,
)
model = OpenAIModel(
    plugin_config.prompt,
    plugin_config.token,
    plugin_config.model_name,
    plugin_config.base_url,
)
HTTPX_CLIENT = httpx.AsyncClient()

summary = on_alconna(
    Alconna(
        "省流",
        Option("-n", Args["num?", int]),
        Option("-i", Args["id?", str]),
        Option("-g", Args["group?", str]),
        Option("-t", Args["time?", str]),
    ),
    extensions=[ReplyRecordExtension()],
    aliases={"总结", "总结一下"},
    use_cmd_start=True,
    priority=5,
    block=True,
)


@summary.handle()
async def _(
    bot: Bot,
    event: Event,
    num:Match[int],
    id:Match[str],
    group:Match[str],
    time:Match[str],
    ext: ReplyRecordExtension,
    msg_id:MsgId,
    session: Session = Depends(extract_session)
):  
    if reply := ext.get_reply(msg_id):
        reply_msg = reply
        if not reply_msg.msg:
            raise Exception("获取消息内容错误，请重试。")
        if isinstance(reply_msg.msg, str):
            reply_msg = reply_msg.msg
        else:
            reply_msg = reply_msg.msg.extract_plain_text()

        if match := re.match(r"^(https?|http?):\/\/([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}|localhost)(:\d{2,5})?(\/[a-zA-Z0-9._%+-\/\?=&#]*)?$", reply_msg):
            res = await HTTPX_CLIENT.get(match[0])
            reply_msg = res.text
        
        await model.set_prompt(plugin_config.url_prompt)
        response = await model.summary(reply_msg)
        if plugin_config.aggregate_message:
            await saa.AggregatedMessageFactory([saa.Text(response)]).finish()
        else:
            await saa.Text(response).finish(reply=True)

    if group.available:
        group_id = [group.result]
    elif session.id2:
        group_id = [session.id2]
    else:
        await saa.Text("请指定群聊或在群聊中使用").finish()
    
    if num.available:
        number = num.result
    else:
        number = plugin_config.default_context
    
    if id.available:
        user_id = [id.result]
    else:
        user_id = None
    
    dt = get_datetime_now_with_timezone()
    time_start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    time_stop = dt
    if time.available:
        time_ = time.result
        if match := re.match(r"^(.+?)(?:~(.+))?$", time_):
                start = match[1]
                stop = match[2]
                time_start = get_datetime_fromisoformat_with_timezone(start)
                time_stop = get_datetime_fromisoformat_with_timezone(stop)

    if not time_start or not time_stop:
        await saa.Text("请正确输入时间格式，例如：2024-01-01~2024-01-14，不然我没法理解哦~").finish()
    
    raw_record = await get_message_records(
        id2s=group_id,
        id1s=user_id,
        time_start=time_start,
        time_stop=time_stop,
    )
    raw_record = raw_record[-number:]
    record = await build_records(bot, event, raw_record)
    response = await model.summary(record)
    if plugin_config.aggregate_message:
        await saa.AggregatedMessageFactory([saa.Text(response)]).finish()
    else:
        await saa.Text(response).finish(reply=True)
