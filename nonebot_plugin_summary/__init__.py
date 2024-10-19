from nonebot import require

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
require("nonebot_plugin_chatrecorder")
import nonebot_plugin_saa as saa
from nonebot_plugin_alconna import Alconna, Args, Command, Match, Option, on_alconna
from nonebot_plugin_session import Session, extract_session

from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.adapters import Bot, Event
from nonebot.params import Depends

from .utils import __usage__, get_records, build_records, OpenAIModel
from .config import Config, plugin_config

__plugin_meta__ = PluginMetadata(
    name="B话排行榜",
    description="调查群U的B话数量，以一定的顺序排序后排序出来。",
    usage=__usage__,
    homepage="https://github.com/ChenXu233/nonebot_plugin_dialectlist",
    type="application",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_chatrecorder", "nonebot_plugin_saa", "nonebot_plugin_alconna"
    ),
    config=Config,
)

summary = on_alconna(
    Alconna(
        "省流",
        Option("-n", Args["num?",int]),
        Option("-i", Args["id?",str]),
        Option("-g", Args["group?",str]),
        Option("-t", Args["time?",str]),
    ),
    aliases={"总结", "总结一下"},
    use_cmd_start=True,
    priority=5,
    block=True,
)

@summary.handle()
async def _(bot: Bot, event: Event,session: Session = Depends(extract_session)):
    model = OpenAIModel(plugin_config.prompt,plugin_config.token,plugin_config.model_name,plugin_config.base_url)
    raw_record = await get_records(session)
    record = await build_records(bot,event,raw_record)
    reponse = await model.summary(record)
    await saa.Text(reponse).send(reply=True)