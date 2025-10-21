from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random  # 新增：用于随机选择回复

@register("astrbot_plugin_ceshi", "mookoo", "小碎bot测试中。", "v1.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名改为「小碎」
    @filter.command("小碎")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令"""  # 保持原注释不变
        user_name = event.get_sender_name()
        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)

        # 新增：候选回复（5~6 条），触发后随机选一条
        replies = [
            f"你好呀，{user_name}，小碎在这里～",
            f"{user_name}，小碎到咯！找我有什么事吗？",
            f"在呢在呢～{user_name}，小碎随时待命！",
            f"喵？是{user_name}在叫我吗～小碎已上线！",
            f"嘿嘿，{user_name}，小碎来了！需要帮忙的话尽管说～",
            f"报告！{user_name}，小碎就位！(￣▽￣)ゞ"
        ]
        yield event.plain_result(random.choice(replies))  # 随机发送一条

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

