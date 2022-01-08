import discord
from discord.ext import commands
from colorama import Fore
from asyncio import sleep
import requests
import random
import json

with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)
reaction=False

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def type(self, ctx, *, text):
		message=f'{text[0]}'
		await ctx.message.edit(content=message)
		for c in text[1:]:
			message+=c
			await ctx.message.edit(content=message)
			await sleep(0.5)
	@commands.command()
	async def faketyping(self, ctx, amount: int):
		await ctx.message.delete()
		for i in range(amount):
			response=requests.post(f"https://discord.com/api/v9/channels/{ctx.channel.id}/typing", headers={"authorization": config['TOKEN']})
			await sleep(3)
	@commands.command()
	async def boom(self, ctx):
		await ctx.message.edit(content="**Данный чат будет взорван через 5 секунд...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 4 секунды...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 3 секунды...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 2 секунды...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 1 секунду...**")
		await sleep(1)
		await ctx.message.delete()
		message=await ctx.send("**Boom!**", file=discord.File("Resources/boom.gif"))
		await sleep(1)
		await ctx.send("⠀" + "\n"*1998 + "⠀")
		await message.delete()
	@commands.command()
	async def embed(self, ctx, *, text):
		embed=discord.Embed(title=text, color=0x8B0000)
		await ctx.message.edit(content='', embed=embed)
	@commands.command()
	async def hack(self, ctx, *, user: discord.User):
		perc=0
		while(perc < 100):
			text =f"‍Взлом аккаунта {user} в процессе... " + str(perc) + "%"
			await ctx.message.edit(content=text)
			perc += random.randint(1, 8)
		response=requests.get(f"https://some-random-api.ml/bottoken?id={user.id}").json()
		token=response['token']
		await ctx.message.edit(content=f"Токен {user}: `{token}`")
	@commands.command()
	async def reactionbot(self, ctx):
		global reaction
		if reaction==True:
			reaction=False
			await ctx.message.edit(content="**:white_check_mark: Reaction Bot был успешно выключен!**", delete_after=3)
		elif reaction==False:
			reaction=True
			await ctx.message.edit(content="**:white_check_mark: Reaction Bot был успешно включён!**", delete_after=3)
	@commands.Cog.listener()
	async def on_message(self, message):
		global reaction
		if reaction==True:
			try: await message.add_reaction(config['Emoj_Reaction'])
			except: pass
	@commands.command()
	async def reactionall(self, ctx, amount: int):
		await ctx.message.delete()
		messages = await ctx.channel.history(limit=amount).flatten()
		reactioned=0
		for message in messages:
			await message.add_reaction(config['Emoj_Reaction'])
			reactioned+=1
		print(Fore.WHITE + f"[LOG] Успешно поставил реакциии на {reactioned} сообщений!")
		await ctx.send(f"**:white_check_mark: Успешно поставил реакциии на {reactioned} сообщений!**", delete_after=5)
	@commands.command()
	async def lags(self, ctx):
		await ctx.message.edit(content=":chains:"*250)
		for i in range(49):
			await ctx.send(":chains:"*250)
		print(Fore.WHITE + f"[LOG] Успешно сделал лаги!")
def setup(bot):
	bot.add_cog(Fun(bot))