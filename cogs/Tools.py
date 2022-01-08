import discord
from discord.ext import commands
import requests
from asyncio import sleep
from colorama import Fore
import random, string
import json
from time import time as time1

class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def webhookspam(self, ctx, webhook, amount:int, *, message):
		await ctx.message.delete()
		for i in range(amount):
			while True:
				try: response=requests.post(webhook, json={"content": message})
				except:
					await ctx.send("**:x: Вебхук нерабочий!**", delete_after=5)
					return
				if response.status_code==204:
					print(Fore.WHITE + "[LOG] Отправил сообщение на вебхук!")
					break
				elif response.status_code==429:
					json_data = json.loads(response.text)
					if 100 > json_data['retry_after']:
						await sleep(json_data['retry_after'])
				elif response.status_code==404:
					await ctx.send(content="**:x: Вебхук нерабочий!**", delete_after=5)
					return
				else:
					pass
		print(Fore.WHITE + f"[LOG] Успешно отправил на вебхук {amount} сообщений!")
		await ctx.send(f"**:white_check_mark: Успешно отправил на вебхук {amount} сообщений!**", delete_after=5)
	@commands.command()
	async def status(self, ctx, aboba=None, *, Name=None):
		if aboba == "Playing" or aboba =="Game":
			await ctx.message.delete()
			await self.bot.change_presence(activity=discord.Game(name=Name))
		elif aboba == "Watching":
			await ctx.message.delete()
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=Name))
		elif aboba == "Listening":
			await ctx.message.delete()
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=Name))
		elif aboba == "Streaming":
			await ctx.message.delete()
			await self.bot.change_presence(activity=discord.Streaming(name=Name, url="https://www.twitch.tv/discord"))
		else:
			await ctx.message.edit(content="**Доступные варианты: `Watching`, `Listening`, `Playing`, `Streaming`**", delete_after=5)
	@commands.command()
	async def spam(self, ctx, amount: int, *, text):
		amogus = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
		await ctx.message.edit(content=f"{text} ||{amogus}||")
		for i in range(amount-1):
			amogus = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
			await ctx.send(f"{text} ||{amogus}||")
		print(Fore.WHITE + "[LOG] Спам завершён!")
		await ctx.send("**:white_check_mark: Спам завершён!**", delete_after=5)
	@commands.command()
	async def spamall(self, ctx, amount: int, *, text):
		amogus = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
		await ctx.message.edit(content=f"{text} ||{amogus}||")
		for i in range(amount):
			for channel in ctx.guild.text_channels:
				amogus = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
				try: await channel.send(f"{text} ||{amogus}||")
				except: pass
		print(Fore.WHITE + "[LOG] Спам завершён!")
		await ctx.send("**:white_check_mark: Спам завершён!**", delete_after=5)
	@commands.command()
	async def pingall(self, ctx):
		roles=[]
		for role in ctx.guild.roles:
			if role.mentionable:
				roles.append(role.mention)
		if roles==[]:
			await ctx.message.edit(content="**:warning: Нет ролей которые можно пинговать!**", delete_after=3)
		else:
			await ctx.message.delete()
			await ctx.send(''.join(roles))
	@commands.command()
	async def purge(self, ctx, amount: int):
		await ctx.message.delete()
		messages = await ctx.channel.history(limit=amount).flatten()
		deleted=0
		for message in messages:
			if message.author.id==self.bot.user.id:
				await message.delete()
				deleted+=1
		print(Fore.WHITE + f"[LOG] Успешно удалил {deleted} сообщений!")
		await ctx.send(f"**:white_check_mark: Успешно удалил {deleted} сообщений!**", delete_after=5)
	@commands.command()
	async def calc(self, ctx, aboba):
		if "+" in aboba:
			numbers=aboba.split("+")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"{number1}+{number2}={number1+number2}")
		if "-" in aboba:
			numbers=aboba.split("-")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"{number1}-{number2}={number1-number2}")
		if "*" in aboba:
			numbers=aboba.split("*")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"{number1}*{number2}={number1*number2}")
		if "/" in aboba:
			numbers=aboba.split("/")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"{number1}/{number2}={number1/number2}")
def setup(bot):
	bot.add_cog(Tools(bot))