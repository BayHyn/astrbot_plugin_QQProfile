from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp
from astrbot.core.platform import AstrMessageEvent
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)
from astrbot.core.star.filter.permission import PermissionType
from .status import status_mapping


@register(
    "astrbot_plugin_QQProfile",
    "Zhalslar",
    "[仅aiocqhttp] 配置bot的头像、昵称、签名、状态、机型等QQ资料",
    "v1.1.1",
)
class QQProfilePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置头像", desc="将引用的图片设置为头像")
    async def set_avatar(self, event: AstrMessageEvent):
        messages = event.get_messages()
        img_url = None
        for seg in messages:
            if isinstance(seg, Comp.Image):
                img_url = seg.url
                break
            elif isinstance(seg, Comp.Reply):
                if seg.chain:
                    for reply_seg in seg.chain:
                        if isinstance(reply_seg, Comp.Image):
                            img_url = reply_seg.url
                            break

        if img_url:
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot
            await client.set_qq_avatar(file=img_url)
            yield event.plain_result("我头像更新啦>v<")
        else:
            yield event.plain_result("找不到图片")

    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置昵称", desc="设置Bot的昵称")
    async def set_nickname(self, event: AiocqhttpMessageEvent, nickname: str|None = None):
        if not nickname:
            yield event.plain_result("没提供新昵称呢")
            return
        client = event.bot
        await client.set_qq_profile(nickname=nickname)
        yield event.plain_result(f"我昵称已改为【{nickname}】")

    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置签名", desc="设置Bot的签名，并同步空间（可在QQ里关掉）")
    async def set_longnick(self, event: AiocqhttpMessageEvent, longnick: str|None = None):
        if not longnick:
            yield event.plain_result("没提供新签名呢")
            return
        client = event.bot
        await client.set_self_longnick(longNick=longnick)
        yield event.plain_result(f"我签名已更新：{longnick}")

    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置状态", desc="设置Bot的在线状态")
    async def set_status(self, event: AiocqhttpMessageEvent, status_name: str|None = None):
        if not status_name:
            yield event.plain_result("没提供新状态呢")
            return
        client = event.bot
        params = status_mapping.get(status_name, None)
        if not params:
            yield event.plain_result(f"状态【{status_name}】暂未支持")
            return
        await client.set_online_status(
            status=params[0], ext_status=params[1], battery_status=0
        )
        yield event.plain_result(f"我状态已更新为【{status_name}】")
