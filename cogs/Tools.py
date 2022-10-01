import discord
from discord.ext import commands
import random, string
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
	async def pingall(self, ctx, amount: int=1):
		await ctx.message.delete()
		for i in range(amount):
			text=''
			pinged=0
			for i in ctx.guild.members:
				if len(text)>=1950:
					await ctx.send(text)
					text=''
				if not i.bot and i.id!=self.bot.user.id:
					text+=i.mention
					pinged+=1
			await ctx.send(text)
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно пинганул {pinged} пользователей {amount} раз!**")
	@commands.command(aliases=['copy', 'сообщения', 'сохранить'])
	async def messages(self, ctx, amount: int=30):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		messages.reverse()
		saved=0
		with open(f'messages_{ctx.channel.id}.txt', 'w', encoding='utf-8') as f:
			for message in messages:
				f.write(f'[{message.author}]: {message.content}\n')
				saved+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно сохранил {saved} сообщений!**", file=discord.File(f'messages_{ctx.channel.id}.txt'))
	@commands.command(aliases=['leavegroups', 'leavegroup', 'groupleave'])
	async def groupsleave(self, ctx):
		leaved=0
		for group in self.bot.private_channels:
			if not 'Direct Message' in str(group) and not str(group).lower()=='избранное': 
					await group.leave()
					leaved+=1
		await ctx.message.edit(content=f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно вышел из {leaved} групп!**")
	@commands.command(aliases=['floodall', 'спамалл', 'флудалл'])
	async def spamall(self, ctx, amount: int, *, text):
		await ctx.message.delete()
		for i in range(amount):
			for channel in ctx.guild.text_channels:
				try: await channel.send(f'{text} ||{"".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))}||')
				except: pass
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно отправил по {amount} сообщений в каждый канал!**")
def setup(bot):
	bot.add_cog(Tools(bot))
