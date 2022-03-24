import discord
from discord.ext import commands
import requests
import random, string
import json
from time import sleep
from threading import Thread
from colorama import init, Fore;init()

with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)
cleanmessage=0

def Flooder(id, message):
	while True:
		adad = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
		response=requests.post(f"https://discord.com/api/v9/channels/{id}/messages", headers={'Authorization': config['Token']}, json={"content": message + f" ||{adad}||"})
		if response.status_code==429:
			json_data = json.loads(response.text)
			sleep(json_data['retry_after'])
		elif not response.status_code==200:
			break
class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def invite(self, ctx, user:discord.User):
		if not user.bot:
			await ctx.message.edit(content='**:warning: Данный аккаунт не является ботом**', delete_after=3)
			return
		await ctx.message.edit(content=f'https://discord.com/api/oauth2/authorize?client_id={user.id}&permissions=8&scope=bot%20applications.commands')
	@commands.command()
	async def short(self, ctx, *, link):
		response=requests.get(f'https://clck.ru/--?url={link}')
		await ctx.message.edit(content=f'<{response.text}>')
	@commands.command()
	async def spam(self, ctx, *, text):
		await ctx.message.edit(content=text)
		for i in range(5):
			Thread(target=Flooder, args=(ctx.channel.id, text)).start()
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
	async def purge(self, ctx, amount: int):
		await ctx.message.delete()
		messages = await ctx.channel.history(limit=amount).flatten()
		deleted=0
		for message in messages:
			if message.author.id==self.bot.user.id:
				await message.delete()
				deleted+=1
		await ctx.send(f"**:white_check_mark: Успешно удалил {deleted} сообщений!**", delete_after=5)
	@commands.command()
	async def calc(self, ctx, aboba):
		if "+" in aboba:
			numbers=aboba.split("+")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"**{number1}+{number2}=`{number1+number2}`**")
		elif "-" in aboba:
			numbers=aboba.split("-")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"**{number1}-{number2}=`{number1-number2}`**")
		elif "*" in aboba:
			numbers=aboba.split("*")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"**{number1}*{number2}=`{number1*number2}`**")
		elif "/" in aboba:
			numbers=aboba.split("/")
			number1=int(numbers[0])
			number2=int(numbers[1])
			await ctx.message.edit(content=f"**{number1}/{number2}=`{number1/number2}`**")
		else:
			await ctx.reply('**:warning: Неверный оператор!**')
	@commands.command()
	async def pingall(self, ctx):
		await ctx.message.delete()
		text=''
		for i in ctx.guild.members:
			if len(text)>=1950:
				await ctx.send(text)
				text=''
			if not i.bot and i.id!=self.bot.user.id:
				text+=i.mention
		await ctx.send(text)
		print(f'{Fore.WHITE}[LOG] Успешно пинганул всех на сервере {Fore.CYAN}{ctx.guild.name}{Fore.WHITE}!')
	@commands.command()
	async def getallusers(self, ctx):
		await ctx.message.delete()
		text=''
		for i in ctx.guild.members:
			if not i.bot:
				text+=str(i.id)+'\n'
		with open(f'users_{ctx.guild.id}.txt', 'w', encoding='utf-8') as f:
			f.write(text)
		print(f'{Fore.WHITE}[LOG] Успешно записал всех участников сервера {Fore.CYAN}{ctx.guild.name}{Fore.WHITE} в {Fore.CYAN}users_{ctx.guild.id}.txt{Fore.WHITE}!')
	@commands.command()
	async def clean(self, ctx):
		message=await ctx.send('**Вы уверены что хотите полностью очистить данный аккаунт?\nЧтобы начать очистку измените это сообщение.\n\n:warning: Очистка удалит все сервера, друзей и лс!**')
		global cleanmessage
		cleanmessage=message.id
		await ctx.message.delete()
	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if before.content==after.content:
			return
		if before.id==cleanmessage:
			for guild in self.bot.guilds:
				try: await guild.leave()
				except: await guild.delete()
			for user in self.bot.user.friends:
				await user.remove_friend()
			for channel in self.bot.private_channels:
				while True:
					response=requests.delete(f"https://discord.com/api/v9/channels/{channel.id}", headers={'Authorization': config['Token']})
					if response.status_code!=401:
						break
					sleep(response.json()['retry_after'])
			print(Fore.WHITE+'[LOG] Очистка прошла успешно!')
	@commands.command()
	async def massdm(self, ctx, *, text):
		for user in self.bot.user.friends:
			await user.send(text)
		await ctx.message.edit(content=f'**:white_check_mark: Успешно отправил всем друзьям сообщение `{text}`**', delete_after=5)
def setup(bot):
	bot.add_cog(Tools(bot))
