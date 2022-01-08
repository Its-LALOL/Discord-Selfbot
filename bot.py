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
os.system(f'cls && title Self bot By LALOL' if os.name == 'nt' else 'clear')
print(LALOL)
print(Fore.GREEN + "Self bot By LALOL\n" + Fore.RED)

bot = commands.Bot(command_prefix=config["PREFIX"], case_insensitive=True, self_bot=True)
bot.remove_command("help")
version=0.1

pref=config['PREFIX']

@bot.event
async def on_ready():
	try: os.remove("version")
	except: pass
	try: os.remove("LICENSE")
	except: pass
	try: os.remove("README.md")
	except: pass
	if not os.path.isdir("Temp"):
		os.mkdir("Temp")
	else:
		for file in os.listdir("./Temp"):
			os.remove(f"Temp/{file}")
	print(Fore.MAGENTA + f"Аккаунт: {Fore.YELLOW}{bot.user}{Fore.MAGENTA}\nid: {Fore.YELLOW}{bot.user.id}{Fore.MAGENTA}\nPrefix: {Fore.YELLOW}{config['PREFIX']}{Fore.RED}\n")
	response=requests.get("https://raw.githubusercontent.com/Its-LALOL/Discord-Selfbot/main/version").text
	response=int(response.replace(".", ''))
	global version
	version1=int(str(version).replace(".", ''))
	aa=response-version1
	if not aa<=0:
		print(Fore.WHITE + f"Было найдено обновление для селф бота!\nДля того чтобы получить ссылку на скачивание напишите команду {Fore.YELLOW}{pref}selfbot{Fore.RED}\n")
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
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")
@bot.command()
async def help(ctx, category=None):
	if category is None:
		embed=discord.Embed(title="Категории Команд", description=f"```{pref}help Tools - Всякие интересные инструменты.\n\n{pref}help Info - Команды с помощью которых вы можете получить информацию о чём либо.\n\n{pref}help Crash - Краш команды.\n\n{pref}help Fun - Всякие приколы и т.д.\n\n{pref}help Token - Команды связанные с токенами.\n\n{pref}selfbot - Информация о селф боте.```", color=0x8B0000)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
		return
	category=category.lower()
	if category=="tools":
		embed=discord.Embed(title="Tools", description=f"```{pref}spam [Количество] [Текст] - Очень хороший спам с обходом анти-спама.\n\n{pref}spamall [Количество] [Текст] - Опять же спам только уже во все каналы.\n\n{pref}calc [Пример] - Обыкновенный калькулятор.\n\n{pref}purge [Количество] - Удаление своих сообщений в этом же канале.\n\n{pref}pingall - Пинг всех ролей которые пингуется (Подойдёт для рейда).\n\n{pref}status [Тип] [Текст] - Изменение статуса.\n\n{pref}webhookspam [Вебхук] [Количество] [Текст] - Спамит сообщениями через вебхук.```", color=0x8B0000)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	elif category=="info":
		embed=discord.Embed(title="Info", description=f"```{pref}getchannels - Получает и отправляет все каналы.\n\n{pref}getroles - Получает и отправляет все роли.\n\n{pref}getemojis - Получает и отправляет все эмодзи.\n\n{pref}guild - Информация о сервере.\n\n{pref}invite [Ссылка Приглашения] - Информация о ссылке приглашения.\n\n{pref}user [Пользователь] - Показывает информацию о Аккаунте.\n\n{pref}channel [id] - Показывает информацию о канале.\n\n{pref}role [id] - Показывает информацию о роле.\n\n{pref}emoji [id] - Показывает информацию о эмодзи.```", color=0x8B0000)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	elif category=="crash":
		embed=discord.Embed(title="Crash", description=f"```{pref}nuke - Удаляет все каналы, роли и эмодзи.\n\n{pref}spamchannels - Создаёт максимальное количество спам каналов.\n\n{pref}spamroles - Создаёт максимальное количество спам ролей.\n\n{pref}spamemojis [Файл] - Создаёт очень много эмодзи с картинкой которую вы прикрепили.\n\n{pref}webhooksspam [Сообщение] - Спамит всеми вебхуками которые есть на сервере.\n\n{pref}deletechannels - Удаляет все каналы.\n\n{pref}deleteroles - Удаляет все роли.\n\n{pref}deleteemojis - Удаляет все эмодзи.```", color=0x8B0000)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	elif category=="fun":
		embed=discord.Embed(title="Fun", description=f"```{pref}type [Текст] - Набирает текст по буквам.\n\n{pref}embed [Текст] - Отправляет текст в эмбеде.\n\n{pref}boom - Взрыв чата.\n\n{pref}hack [Пользователь] - Фейковый взлом Аккаунта.\n\n{pref}reactionbot - Включает/Выключает ReactionBot'а который ставит реакции на все новые сообщения.\n\n{pref}reactionall [Количество] - Ставит реакции на прошлые сообщения.\n\n{pref}faketyping [Количество] - Делает фейковую печать (1 = 3 секунды).\n\n{pref}lags - Делает очень сильные лаги в канале```", color=0x8B0000)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	elif category=="token":
		embed=discord.Embed(title="Token", description=f"```{pref}token [Токен] - Показывает информацию о токене.\n\n{pref}nuketoken [Токен] - Полностью уничтожает аккакунт.```", color=0x8B0000)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	else:
		await ctx.message.edit(content="**:warning: Такой категории не существует!**", delete_after=3)
@bot.command()
async def selfbot(ctx):
	embed=discord.Embed(title="Self bot", description=f"**[Скачать Бота](https://github.com/Its-LALOL/Discord-Selfbot/archive/refs/heads/main.zip)\nСоздатель Бота: [LALOL](https://github.com/Its-LALOL)\nGithub: https://github.com/Its-LALOL/Discord-Selfbot\nВерсия: `{version}`**", color=0x8B0000)
	embed.set_footer(text="Self bot By LALOL")
	await ctx.message.edit(content='', embed=embed)
try: bot.run(config["TOKEN"], bot=False)
except:
	while True:
		input("Invalid Token!")
