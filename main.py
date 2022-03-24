import discord
from discord.ext import commands
from colorama import init, Fore;init()
import os
import json
import requests

with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

LALOL=Fore.RED +"""
██╗░░░░░░█████╗░██╗░░░░░░█████╗░██╗░░░░░
██║░░░░░██╔══██╗██║░░░░░██╔══██╗██║░░░░░
██║░░░░░███████║██║░░░░░██║░░██║██║░░░░░
██║░░░░░██╔══██║██║░░░░░██║░░██║██║░░░░░
███████╗██║░░██║███████╗╚█████╔╝███████╗
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░╚══════╝
"""
os.system(f'cls && title Selfbot By LALOL' if os.name == 'nt' else 'clear')
print(LALOL)
print(Fore.GREEN + "Selfbot By LALOL\n" + Fore.RED)


pref=config['Prefix']

bot = commands.Bot(command_prefix=pref, case_insensitive=True, self_bot=True)
version=0.1

@bot.event
async def on_ready():
	for filename in os.listdir():
		if filename.endswith('.txt'):
			os.remove(filename)
	print(Fore.MAGENTA + f"Аккаунт: {Fore.YELLOW}{bot.user}{Fore.MAGENTA}\nID: {Fore.YELLOW}{bot.user.id}{Fore.MAGENTA}\nPrefix: {Fore.YELLOW}{pref}{Fore.RED}\n")
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		print(Fore.RED + f"[ERROR] Недостаточно аргументов!")
	elif isinstance(error, commands.CommandNotFound):
		print(Fore.RED + f"[ERROR] Данной команды не существует!")
	elif isinstance(error, commands.BadArgument):
		print(Fore.RED + f"[ERROR] Неправильный аргумент!")
	else:
		print(Fore.RED + f"[ERROR] {error}")
@bot.command()
async def bot(ctx):
	await ctx.message.edit(content='**Selfbot By LALOL\n\nСсылка: https://github.com/Its-LALOL/Discord-Selfbot **')
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")
try: bot.run(config["Token"])
except:
	while True:
		input("Invalid Token!")
