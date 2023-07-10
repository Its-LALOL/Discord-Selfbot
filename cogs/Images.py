import discord
from discord.ext import commands
import requests
import random, string
from urllib.parse import quote
from qrcode import make as qrmake

class Images(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['лгбт'])
	async def lgbt(self, ctx, victim:discord.User):
		await ctx.message.edit(content=f'** https://some-random-api.ml/canvas/gay?avatar={victim.avatar_url_as(static_format="png")} **')
	@commands.command(aliases=['тюрьма'])
	async def jail(self, ctx, victim:discord.User):
		await ctx.message.edit(content=f'** https://some-random-api.ml/canvas/jail?avatar={victim.avatar_url_as(static_format="png")} **')
	@commands.command(aliases=['комментарий'])
	async def comment(self, ctx, victim:discord.User, *, text):
		await ctx.message.edit(content=f'** https://some-random-api.ml/canvas/youtube-comment?username={quote(victim.name)}&avatar={victim.avatar_url_as(static_format="png")}&comment={quote(text)} **')
	@commands.command(aliases=['changemymind', 'change-my-mind', 'change_my_mind'])
	async def cmm(self, ctx, *, text):
		link=requests.get(f'https://nekobot.xyz/api/imagegen?type=changemymind&text={quote(text)}').json()['message']
		await ctx.message.edit(content=f'** {link} **')
	@commands.command(aliases=['foxes', 'foxi', 'лис','лиса', 'лисы'])
	async def fox(self, ctx):
		link=requests.get('https://randomfox.ca/floof/').json()['link']
		await ctx.message.edit(content=f'** {link} **')
	@commands.command()
	async def lightshot(self, ctx, amount: int=1):
		await ctx.message.delete()
		for i in range(amount):
			text=''
			for i in range(5):
				id=''
				for i in range(6):
					id+=random.choice(string.ascii_lowercase+string.digits)
				text+=f'https://prnt.sc/{id}\n'
			await ctx.send(content=text)
	@commands.command(aliases=['qr'])
	async def qrcode(self, ctx, *, content):
		await ctx.message.delete()
		qrcode=qrmake(content)
		qrcode.save(f'qrcode_{ctx.message.id}.png')
		await ctx.send('** :cd: QRcode был успешно создан!**', file=discord.File(f'qrcode_{ctx.message.id}.png'))
def setup(bot):
	bot.add_cog(Images(bot))
