import discord
from discord.ext import commands
from asyncio import sleep
import requests
from urllib.parse import quote

class Images(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['лгбт'])
	async def lgbt(self, ctx, victim:discord.User):
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nhttps://some-random-api.ml/canvas/gay?avatar={victim.avatar_url_as(static_format="png")} **')
	@commands.command(aliases=['тюрьма'])
	async def jail(self, ctx, victim:discord.User):
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nhttps://some-random-api.ml/canvas/jail?avatar={victim.avatar_url_as(static_format="png")} **')
	@commands.command(aliases=['комментарий'])
	async def comment(self, ctx, victim:discord.User, *, text):
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nhttps://some-random-api.ml/canvas/youtube-comment?username={quote(victim.name)}&avatar={victim.avatar_url_as(static_format="png")}&comment={quote(text)} **')
	@commands.command(aliases=['fake_type', 'фейк_печать','фейкпечать', 'faketype'])
	async def faketyping(self, ctx, seconds:int, channel_id: int=None):
		await ctx.message.delete()
		if channel_id is None: channel=ctx.channel
		else: channel=self.bot.get_channel(channel_id)
		async with channel.typing():
			await sleep(seconds)
	@commands.command(name='reactionbot', aliases=['reaction_bot'])
	async def __reactionbot(self, ctx, emoji='🤡', server_id=None):
		global reactionbot
		if reactionbot['enabled']:
			reactionbot['enabled']=False
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\n:white_check_mark: Reaction Bot был успешно выключен!**")
		else:
			reactionbot['enabled']=True
			reactionbot['emoji']=emoji
			reactionbot['server_id']=server_id
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\n:white_check_mark: Reaction Bot был успешно включён!**")
	@commands.command(aliases=['лиса', 'лисы'])
	async def fox(self, ctx):
		link=requests.get('https://some-random-api.ml/img/fox').json()['link']
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n{link}**')
	@commands.command(aliases=['собака', 'собаки', 'dogs'])
	async def dog(self, ctx):
		link=requests.get('https://some-random-api.ml/img/dog').json()['link']
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n{link} **')
	@commands.command(aliases=['кот', 'коты', 'кошечка', 'cats'])
	async def cat(self, ctx):
		link=requests.get('https://some-random-api.ml/img/cat').json()['link']
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n{link} **')
	@commands.command(aliases=['панда', 'панды'])
	async def panda(self, ctx):
		link=requests.get('https://some-random-api.ml/img/panda').json()['link']
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n{link} **')
	@commands.command(aliases=['коала', 'коалы'])
	async def koala(self, ctx):
		link=requests.get('https://some-random-api.ml/img/koala').json()['link']
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n{link} **')
def setup(bot):
	bot.add_cog(Images(bot))
