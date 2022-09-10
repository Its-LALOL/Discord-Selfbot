import discord
from discord.ext import commands
import random, string
from asyncio import sleep
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['статус', 'activity', 'активность'])
	async def status(self, ctx, cat='ы', *, name='Selfbot by LALOL'):
		status=config['Status']
		sstatus=discord.Status.online
		if status=='idle':
			sstatus=discord.Status.idle
		if status=='dnd':
			sstatus=discord.Status.dnd
		if status=='invisible':
			sstatus=discord.Status.invisible
		cat=cat.lower()
		game=['play', 'playing', 'играть', 'играет', 'game', 'игра', 'играю']
		watching=['watching', 'watch', 'смотреть', 'смотрит', 'смотрю']
		listening=['listening', 'listen', 'слушает', 'слушать', 'слушаю']
		streaming=['streaming', 'stream', 'стрим', 'стримить', 'стримлю', 'стримит']
		reset=['reset', 'remove', 'none', 'off', 'убрать', 'выключить', 'обычный', 'ресет', 'delete', 'удалить']
		if cat in game:
			await self.bot.change_presence(status=sstatus, activity=discord.Game(name=name))
		elif cat in watching:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.watching, name=name))
		elif cat in listening:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.listening, name=name))
		elif cat in streaming:
			await self.bot.change_presence(status=sstatus, activity=discord.Streaming(name=name, url="https://www.youtube.com/watch?v=yNIQi6cbk2s"))
		elif cat in reset:
			await self.bot.change_presence(status=sstatus, activity=None)
		else:
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\nДоступные варианты: `Watching`, `Listening`, `Playing`, `Streaming` и `Reset`**")
			return
		await ctx.message.edit(content='**__Selfbot by LALOL__\n\n:white_check_mark: Ваш статус был успешно изменён!**')
	@commands.command(alises=['clean', 'clear', 'очистка', 'очистить'])
	async def purge(self, ctx, amount: int):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		deleted=0
		for message in messages:
			if message.author.id==self.bot.user.id:
				await message.delete()
				deleted+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно удалил {deleted} сообщений!**")
	@commands.command(aliases=['spampin', 'pinspam', 'pinmass', 'pin', 'закрепить'])
	async def masspin(self, ctx, amount: int=15):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		pinned=0
		for message in messages:
			try: await message.pin()
			except: pass
			pinned+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно закрепил {pinned} сообщений!**")
	@commands.command(aliases=['спам', 'flood', 'флуд'])
	async def spam(self, ctx, amount: int, *, text):
		await ctx.message.delete()
		for i in range(amount):
			await ctx.send(f'{text} ||{"".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))}||')
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно отправил {amount} сообщений!**")
	@commands.command(aliases=['пингалл'])
	async def pingall(self, ctx):
		await ctx.message.delete()
		text=''
		pinged=0
		for i in ctx.guild.members:
			pinged+=1
			if len(text)>=1950:
				await ctx.send(text)
				text=''
			if not i.bot and i.id!=self.bot.user.id:
				text+=i.mention
		await ctx.send(text)
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно пинганул {pinged} пользователей!**")
def setup(bot):
	bot.add_cog(Tools(bot))
