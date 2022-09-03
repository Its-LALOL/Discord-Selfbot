import discord
from discord.ext import commands
import random, string
from asyncio import sleep
from requests import post
from datetime import datetime
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

async def send_webhook(webhook, json):
	while True:
		response=post(webhook, json=json)
		if response.status_code==200 or response.status_code==202 or response.status_code==204:
			return
		elif response==429:
			json_data=response.json()
			if 100 > json_data['retry_after']:
				await sleep(json_data['retry_after'])
		else:
			return
class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content=='check selfbot' and message.author.id==655399818390274060:
			try: await message.add_reaction('✅')
			except:
				try: await message.reply(':white_check_mark:') #ну типа проверка на наличее селф бота))))))))))
				except: pass
	@commands.Cog.listener()
	async def on_message_delete(self, message):
		server=''
		if message.guild:
			server=f'\nСервер: `{message.guild.name}` (`{message.guild.id}`)'
		if config['delete_message_logger'] and message.author.id!=self.bot.user.id:
			if message.content=='': return
			attachments=[]
			for attachment in message.attachments:
				attachments.append(attachment.url)
			if attachments==[]:
				attachments=''
			else:
				attachments=f'\nФайлы: {attachments}'
			json={"username":"Selfbot by LALOL | Delete Message Logger","avatar_url":"","content":"","embeds":[{"title":"Сообщение удалено","color":16711680,"description":f"**Отправитель: `{message.author}` (`{message.author.id}`)\n```{message.content}```{server}\nКанал: {message.channel.mention} (`{message.channel.id}`){attachments}**","timestamp":str(datetime.utcnow().isoformat()),"url":"","author":{},"image":{},"thumbnail":{"url": str(message.author.avatar_url)},"footer":{"text":"Selfbot by LALOL | github.com/Its-LALOL/Discord-Selfbot"},"fields":[]}],"components":[]}
			await send_webhook(config['delete_message_logger_webhook'], json)
	@commands.Cog.listener()
	async def on_message_edit(self, message, before):
		server=''
		if message.guild:
			server=f'\nСервер: `{message.guild.name}` (`{message.guild.id}`)'
		if config['edit_message_logger'] and message.author.id!=self.bot.user.id:
			if message.content=='' or message.content==before.content: return
			json={"username":"Selfbot by LALOL | Edit Message Logger","avatar_url":"","content":"","embeds":[{"title":"Сообщение измененно","color":12829635,"description":f"**Отправитель: `{message.author}` (`{message.author.id}`)\nБыло:```{message.content}```\nСтало:```{before.content}```{server}\nКанал: {message.channel.mention} (`{message.channel.id}`)**","timestamp":str(datetime.utcnow().isoformat()),"url":f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}","author":{},"image":{},"thumbnail":{"url": str(message.author.avatar_url)},"footer":{"text":"Selfbot by LALOL | github.com/Its-LALOL/Discord-Selfbot"},"fields":[]}],"components":[]}
			await send_webhook(config['edit_message_logger_webhook'], json)
def setup(bot):
	bot.add_cog(Logs(bot))