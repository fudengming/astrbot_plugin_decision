import random

from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp


@register("Decision", "ButterBlock233", "让机器人帮你做决定", "1.1.0")
class DecisionPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.choice_template: str = config.get(
            "choice_template", "🤔 我建议: {choice}！"
        )
        self.none_options: str = config.get(
            "none_options",
            "请提供至少一个选项，例如：/{command_name} 选项1 选项2 选项3",
        )
        self.user_at_space: bool = config.get("user_at_space", False)

    @filter.command("decision", alias={"决定", "建议"})
    async def decision(self, event: AstrMessageEvent):
        """让机器人帮你做决定。用法: /decision 选项1 选项2 选项3..."""
        full_message: str = event.message_str.strip()
        parts = full_message.split()

        command_name = parts[0]
        user_name: str = event.get_sender_name()
        options = parts[1:]

        if not options:
            chain = await self._create_template_result(
                event, self.none_options, user_name=user_name, command_name=command_name
            )
            yield event.chain_result(chain)
            return

        choice = random.choice(options)
        chain = await self._create_template_result(
            event, self.choice_template, user_name=user_name, choice=choice
        )
        yield event.chain_result(chain)

    async def _create_template_result(
        self, event: AstrMessageEvent, template: str, **format_kwargs: any
    ) -> list:
        """处理模板消息并转换为消息链"""

        if "{user_at}" not in template:
            return [Comp.Plain(template.format(**format_kwargs))]

        chain: list = []
        components = template.split("{user_at}")

        for i, component in enumerate(components):
            # 添加文本部分
            prefix = " " if (i > 0 and self.user_at_space) else ""
            chain.append(Comp.Plain(prefix + component.format(**format_kwargs)))

            # 添加 @ 部分
            if i < len(components) - 1:
                chain.append(Comp.At(qq=event.get_sender_id()))

        return chain
