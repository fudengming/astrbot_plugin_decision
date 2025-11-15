from random import random
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random


@register("Decision", "ButterBlock233", "让机器人帮你做决定", "1.0.0")
class DecisionPlugin(Star):
	def __init__(self, context: Context):
		super().__init__(context)

	async def initialize(self):
		"""可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

	# # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
	# @filter.command("helloworld")
	# async def helloworld(self, event: AstrMessageEvent):
	# 	"""这是一个 hello world 指令"""  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
	# 	user_name = event.get_sender_name()
	# 	message_str = event.message_str  # 用户发的纯文本消息字符串
	# 	message_chain = (
	# 		event.get_messages()
	# 	)  # 用户所发的消息的消息链 # from astrbot.api.message_components import *
	# 	logger.info(message_chain)
	# 	yield event.plain_result(
	# 		f"Hello, {user_name}, 你发了 {message_str}!"
	# 	)  # 发送一条纯文本消息

	@filter.command("decision")
	async def decision(self, event: AstrMessageEvent):
		"""让机器人帮你做决定。用法: /decision 选项1 选项2 选项3..."""
		full_message = event.message_str.strip()
		
		# 将消息分割成单词列表
		parts = full_message.split()
		
		# 第一个词是命令名，移除它只保留选项
		if parts and parts[0] == "decision":
			options = parts[1:]
		else:
			options = parts
		
		# 验证是否有选项
		if not options:
			yield event.plain_result("请提供至少一个选项，例如：/decision 逛街 打舞萌 写作业")
			return
		
		# 随机选择一个选项
		choice = random.choice(options)
		user_name = event.get_sender_name()
		logger.info(f"{user_name} 使用 decision 命令，选项: {options}, 结果: {choice}")
		
		# 返回结果
		yield event.plain_result(f"🤔 我建议: {choice}！")

	async def terminate(self):
		"""可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
