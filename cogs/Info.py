import discord
from discord.ext import commands
import random, string
from asyncio import sleep
import os
import requests
from colorama import Fore, init;init()

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def download(self, ctx):
		await ctx.message.delete()
		os.mkdir(str(ctx.guild.id))
		os.mkdir(f'{ctx.guild.id}/channels')
		os.mkdir(f'{ctx.guild.id}/roles')
		os.mkdir(f'{ctx.guild.id}/emojis')
		os.mkdir(f'{ctx.guild.id}/members')
		print(Fore.WHITE+'[LOG] Записываю основную информацию сервера...')
		with open(f'{ctx.guild.id}/info.txt', 'w', encoding='utf-8') as f:
			f.write(f'https://github.com/Its-LALOL/Discord-Selfbot\n\nИмя: {ctx.guild.name}\nID: {ctx.guild.id}')
		print(Fore.WHITE+'[LOG] Записываю все каналы...')
		for channel in ctx.guild.channels:
			with open(f'{ctx.guild.id}/channels/{channel.id}.txt', 'w', encoding='utf-8') as f:
				f.write(f'Имя: {channel.name}\nID: {channel.id}\nТип: {channel.type}')
		print(Fore.WHITE+'[LOG] Записываю все роли..')
		for role in ctx.guild.roles:
			with open(f'{ctx.guild.id}/roles/{role.id}.txt', 'w', encoding='utf-8') as f:
				f.write(f'Имя: {role.name}\nID: {role.id}\nЦвет: {role.color}')
		print(Fore.WHITE+'[LOG] Скачиваю все эмодзи...')
		for emoji in ctx.guild.emojis:
			bbb='png'
			if emoji.animated:
				bbb='gif'
			with open(f'{ctx.guild.id}/emojis/{emoji.name}.{bbb}', 'wb') as f:
				f.write(requests.get(emoji.url).content)
		print(Fore.WHITE+'[LOG] Записываю всех участников..')
		for user in ctx.guild.members:
			with open(f'{ctx.guild.id}/members/{user.id}.txt', 'w', encoding='utf-8') as f:
				f.write(f'Имя: {user.name}\nТег: {user.discriminator}\nID: {user.id}')
		print(f'{Fore.WHITE}[LOG] Сервер {Fore.CYAN}{ctx.guild.name}{Fore.WHITE} был успешно скачан в папке {Fore.CYAN}{ctx.guild.id}{Fore.WHITE}!')
def setup(bot):
	bot.add_cog(Info(bot))