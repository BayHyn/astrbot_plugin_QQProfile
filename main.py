

from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp
from astrbot.core.platform import AstrMessageEvent
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from astrbot.core.star.filter.permission import PermissionType
from .status import status_mapping

@register("astrbot_plugin_QQProfile", "Zhalslar", "[仅aiocqhttp]QQ机器人信息配置插件", "1.0.0")
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
                img_url= seg.url
                break
            elif isinstance(seg, Comp.Reply):
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
            yield event.plain_result(f"找不到图片")


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置昵称", desc="设置Bot的昵称")
    async def set_nickname(self, event: AiocqhttpMessageEvent, nickname:str=None):
        client = event.bot
        await client.set_qq_profile(nickname=nickname)
        yield event.plain_result(f"我昵称已改为【{nickname}】")


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置签名", desc="设置Bot的签名，并同步空间（可在QQ里关掉）")
    async def set_longnick(self, event: AiocqhttpMessageEvent, longnick:str=None):
        client = event.bot
        await client.set_self_longnick(longNick=longnick)
        yield event.plain_result(f"我签名已更新：{longnick}")


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("设置状态", desc="设置Bot的在线状态")
    async def set_status(self, event: AiocqhttpMessageEvent, status_name:str=None):
        client = event.bot
        params = status_mapping.get(status_name, None)
        if not params:
            yield event.plain_result(f"状态【{status_name}】暂未支持")
            return
        await client.set_online_status(
            status=params[0],
            ext_status=params[1],
            battery_status=0
        )
        yield event.plain_result(f"我状态已更新为【{status_name}】")


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("点赞列表", desc="查看谁赞了Bot")
    async def get_profile_like(self, event: AiocqhttpMessageEvent):
        """获取自身点赞列表"""
        client = event.bot
        data = await client.get_profile_like()
        reply = ""
        user_infos = data.get('favoriteInfo', {}).get('userInfos', [])
        for user in user_infos:
            if ('nick' in user and user['nick'] and
                    'count' in user and user['count'] > 0):
                reply += f"\n【{user['nick']}】赞了我{user['count']}次"
        if not reply:
            reply = "暂无有效的点赞信息"
        url = await self.text_to_image(reply)
        yield event.image_result(url)


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("清除未读", desc="将所有未读消息标记为已读")
    async def mark_all_as_read(self, event: AiocqhttpMessageEvent):
        client = event.bot
        await client._mark_all_as_read()
        yield event.plain_result(f"已将所有未读消息标记为已读")


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("群列表")
    async def show_groups_info(self, event: AiocqhttpMessageEvent):
        """查看加入的所有群聊信息"""
        client = event.bot
        group_list = await client.get_group_list()
        group_info = "\n".join(f"{g['group_id']}: {g['group_name']}" for g in group_list)
        info = f"【群列表】共加入{len(group_list)}个群：\n{group_info}"
        yield event.plain_result(info)


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("好友列表")
    async def show_friends_info(self, event: AiocqhttpMessageEvent):
        """查看所有好友信息"""
        client = event.bot
        friend_list = await client.get_friend_list()
        friend_info = "\n".join(f"{f['user_id']}: {f['nickname']}" for f in friend_list)
        info = f"【好友列表】共{len(friend_list)}位好友：\n{friend_info}"
        yield event.plain_result(info)


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("退群")
    async def set_group_leave(self, event: AiocqhttpMessageEvent, group_id:int=None):
        """查看所有好友信息"""
        if not group_id:
            yield event.plain_result("要指明退哪个群哟~")
            return

        client = event.bot
        group_list = await client.get_group_list()

        group_ids = [int(group['group_id']) for group in group_list]
        if group_id not in group_ids:
            yield event.plain_result("我没加有这个群")
            return

        await client.set_group_leave(group_id=group_id)
        yield event.plain_result(f"已退出群聊：{group_id}")


    @filter.permission_type(PermissionType.ADMIN)
    @filter.command("删了",alias={'删除好友'})
    async def delete_friend(self, event: AiocqhttpMessageEvent, target_id:int=None):
        """查看所有好友信息"""
        chain = event.get_messages()
        target_id: int = target_id or next(int(seg.qq) for seg in chain if (isinstance(seg, Comp.At)))

        client = event.bot
        friend_list = await client.get_friend_list()

        friend_ids = [int(friend['user_id']) for friend in friend_list]
        if target_id not in friend_ids:
            yield event.plain_result("我没加有这个人")
            return

        await client.delete_friend(group_id=target_id)
        yield event.plain_result(f"已删除好友：{target_id}")










