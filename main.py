import random

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register


@register("Decision", "ButterBlock233", "让机器人帮你做决定", "1.1.0")
class DecisionPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.aliases = {"决定", "建议"}

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("decision", alias={"决定", "建议"})
    async def decision(self, event: AstrMessageEvent):
        """让机器人帮你做决定。用法: /decision 选项1 选项2 选项3..."""
        full_message = event.message_str.strip()

        # 将消息分割成单词列表
        parts = full_message.split()

        # # 第一个词是命令名，移除它只保留选项
        # if parts and parts[0] in "decision" or self.aliases:
        #       options = parts[1:]
        # else:
        #       options = parts

        command_name = parts[0]
        options = parts[1:]

        # 验证是否有选项
        if not options:
            yield event.plain_result(
                f"请提供至少一个选项，例如：/{command_name} 选项1 选项2 选项3"
            )
            return

        # 随机选择一个选项
        choice = random.choice(options)
        user_name = event.get_sender_name()
        logger.info(f"{user_name} 使用 decision 命令，选项: {options}, 结果: {choice}")

        # 返回结果
        yield event.plain_result(f"🤔 我建议: {choice}！")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
