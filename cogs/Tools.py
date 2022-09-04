import discord
from discord.ext import commands
import random, string
from asyncio import sleep

class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['статус', 'activity', 'активность'])
	async def status(self, ctx, cat='ы', *, name='Selfbot by LALOL'):
		cat=cat.lower()
		game=['play', 'playing', 'играть', 'играет', 'game', 'игра', 'играю']
		watching=['watching', 'watch', 'смотреть', 'смотрит', 'смотрю']
		listening=['listening', 'listen', 'слушает', 'слушать', 'слушаю']
		streaming=['streaming', 'stream', 'стрим', 'стримить', 'стримлю', 'стримит']
		reset=['reset', 'remove', 'none', 'off', 'убрать', 'выключить', 'обычный', 'ресет', 'delete', 'удалить']
		if cat in game:
			await self.bot.change_presence(activity=discord.Game(name=name))
		elif cat in watching:
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
		elif cat in listening:
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))
		elif cat in streaming:
			await self.bot.change_presence(activity=discord.Streaming(name=name, url="https://www.twitch.tv/selfbot_by_LALOL"))
		elif cat in reset:
			await self.bot.change_presence(activity=None)
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
def setup(bot):
	bot.add_cog(Tools(bot))
