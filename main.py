# -*- coding: utf-8 -*-
version=2.4
lencommands=0
import os
clear=lambda: os.system(f'cls && title Selfbot {version} - {lencommands} Commands' if os.name == 'nt' else 'clear')
try:
	import discord
	from discord.ext import commands
	from colorama import init, Fore;init()
	import requests
	from plyer import notification
	from googletrans import Translator
	from emoji import EMOJI_DATA
	from qrcode import make
except:
	os.system('pip install -U discord.py-self==1.9.2 colorama requests plyer googletrans==4.0.0rc1 emoji qrcode')
	import discord
	from discord.ext import commands
	from colorama import init, Fore;init()
	import requests
from subprocess import Popen
from time import sleep
from webbrowser import open as webopen
from threading import Thread
from datetime import datetime
import random
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	try: config = json.load(f)
	except Exception as e:
		clear()
		print(e)
		print(Fore.LIGHTBLUE_EX+'\nОшибка конфига')
		while True: sleep(9)

theme=config['GENERAL']['theme']
if theme=='random':
	theme=random.choice(['standart', 'discord', 'hacker', 'beach'])
if theme=='standart':
	color={'Intro': Fore.RED, 'Info_name': Fore.MAGENTA, 'Info_value': Fore.YELLOW}
elif theme=='discord':
	color={'Intro': Fore.LIGHTBLUE_EX, 'Info_name': Fore.WHITE, 'Info_value': Fore.LIGHTCYAN_EX}
elif theme=='hacker':
	color={'Intro': Fore.LIGHTGREEN_EX, 'Info_name': Fore.GREEN, 'Info_value': Fore.WHITE}
elif theme=='beach':
	color={'Intro': Fore.LIGHTYELLOW_EX, 'Info_name': Fore.LIGHTYELLOW_EX, 'Info_value': Fore.LIGHTCYAN_EX}
else:
	clear()
	print(Fore.LIGHTBLUE_EX+'Неизвестная тема')
	while True: sleep(9)
on_command_error=True
Intro=color['Intro']+"""
____  ___       .__ 
\   \/  /___.__.|__|
 \     /<   |  ||  |
 /     \ \___  ||  |
/___/\  \/ ____||__|
      \_/\/         \n"""
lencommands=0
clear()
print(Intro)
print(Fore.WHITE+'Loading...')
pref=config['GENERAL']['prefix']
try: bot=commands.Bot(command_prefix=pref, case_insensitive=True, self_bot=True)
except Exception as e:
	clear()
	print(e)
	print(Fore.LIGHTBLUE_EX+'\nНа странице селфбота написано как решить эту ошибку!!!')
	sleep(3)
	webopen('https://github.com/PuroSlavKing/Discord-Selfbot', 2)
	while True: sleep(9)
bot.remove_command('help')
update=''

async def check(ctx):
	if not config['OTHER']['nuke_commands']:
		await ctx.message.edit(content='**:warning: Краш команды отключены! Для того чтобы включить краш команды измените файл config.json**')
		return False
	return True
def disco_status():
	while True:
		text=''
		lasttext=''
		for i in range(5):
			while True:
				emoji=random.choice(['🔴', '🟢', '🔵', '🟡', '🟣'])
				if not emoji in text:
					text+=emoji
					break
		if text==lasttext: continue
		lasttext=text
		try:requests.patch("https://discord.com/api/v9/users/@me/settings", headers={'authorization': bot.http.token}, json={'custom_status': {'text': text}})
		except:pass
		sleep(5)
@bot.event
async def on_connect():
	global lencommands
	lencommands=len(bot.commands)
	for file in ['LICENSE', 'README.md']:
		try: os.remove(file)
		except: pass
	for file in os.listdir():
		if file.endswith('.txt') or file.endswith('.png'):
			os.remove(file)
	if config['OTHER']['disco_status']: Thread(target=disco_status).start()
#	status=config['GENERAL']['status']
	response=requests.get('https://discord.com/api/users/@me/settings', headers={'authorization': bot.http.token})
	status=response.json()['status']
	sstatus=discord.Status.online
	if status=='idle':
		sstatus=discord.Status.idle
	elif status=='dnd':
		sstatus=discord.Status.dnd
	elif status=='invisible':
		sstatus=discord.Status.invisible
	await bot.change_presence(status=sstatus)
	try:
		channel=bot.get_channel(config['OTHER']['auto_send_channel'])
		for i in config['OTHER']['auto_send_text']:
			await channel.send(i)
	except: pass
	clear()
	print(Intro)
	print(f"{color['Info_name']}Аккаунт: {color['Info_value']}{bot.user}{color['Info_name']}\nID: {color['Info_value']}{bot.user.id}{color['Info_name']}\nPrefix: {color['Info_value']}{pref}")
	if float(requests.get('https://raw.githubusercontent.com/PuroSlavKing/Discord-Selfbot/main/cogs/version').text)>version:
		global update
		update=f':warning: Пожалуйста, обновите селфбота используя команду {pref}bot**\n**'
		print(f'{Fore.CYAN}Пожалуйста, обновите селфбота используя команду {Fore.LIGHTCYAN_EX}{pref}bot{Fore.RESET}{Fore.RED}\n')
		return
	print(Fore.RED)
if on_command_error:
	@bot.event
	async def on_command_error(ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			error=':warning: Недостаточно аргументов!'
		elif isinstance(error, commands.CommandNotFound):
			return
		elif isinstance(error, commands.BadArgument):
			error=':warning: Указан не правильный аргумент!'
		elif isinstance(error, discord.errors.Forbidden):
			error=':warning: Не достаточно прав для выполнения данной команды!'
		error=str(error).replace('Command raised an exception: ', '')
		print(f"{Fore.RED}[ERROR] {error}")
		try: await ctx.send(f'**:warning: Произошла ошибка :x:\n```{error}```**')
		except: pass
@bot.event
async def on_command(ctx):
	time=datetime.now().strftime('%H:%M:%S')
	arguments=ctx.message.content.replace(pref+ctx.invoked_with, '')
	print(f'{Fore.LIGHTWHITE_EX}[{time}] {Fore.LIGHTCYAN_EX}{pref}{ctx.invoked_with}{Fore.LIGHTGREEN_EX}{arguments}{Fore.RESET}')
@bot.event
async def on_message_edit(before, after):
	await bot.process_commands(after)
@bot.command(aliases=['хелп', 'помощь'])
async def help(ctx, cat=None):
	if cat==None:
		await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Разделы⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}help tools** — полезные команды.
**{pref}help info** — команды для получения информации.
**{pref}help fun** — развлекательные команды.
**{pref}help moderation** — команды модерации.
**{pref}help image** — команды связанные с изображениями.
**{pref}help nuke** — команды краша.

⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Debug⟯**✫⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}reload**  — перезагрузить бота.
**{pref}bot**  — ссылка на GitHub.
''')
		return
	cat=cat.lower()
	if cat=='tools':
		await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Tools⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}status [Тип статуса] [Текст]** — меняет статус.
**{pref}purge [Количество]** — удаляет ваши сообщения.
**{pref}clear [Количество]** — удаляет все сообщения.
**{pref}masspin [Количество]** — закрепляет последние сообщения.
**{pref}messages [Количество]** — сохраняет последние сообщения в файл.
**{pref}groupsleave** — выходит из всех групп.
**{pref}blocksend [Пинг/ID] [Текст]** — отправляет сообщение в ЛС, даже если вы добавили пользователя в ЧС.
**{pref}copystatus [Пинг/ID]** — копирует RPC статус.
**{pref}translate [На какой язык] [Текст]** — переводчик.
**{pref}nitro [Количество] [classic/full]** — генерирует нитро (без проверок).
**{pref}copyemojis [ID Сервера на который нужно скопировать]** — копирует эмодзи.
**{pref}hackpurge** — "удаляет" сообщения без прав.
**{pref}deletedms [Имя]** — удаляет ЛС от ботов с указанным именем.
''')
	elif cat=='info':
		await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Info⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}server** — показывает информацию о сервере.
**{pref}user [Пинг/ID]** — показывает информацию о пользователе.
**{pref}token [Токен]** — показывает информацию о токене.
''')
	elif cat=='fun':
		await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Fun⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}trolldelete [Пинг/ID]** — удаление всех сообщений от пользователя.
**{pref}trollreaction [Пинг/ID] [Эмодзи]** — ставит эмодзи на все сообщения пользователя.
**{pref}trollrepeat [Пинг/ID]** — повторение всех сообщений пользователя.
**{pref}trollmove [Количество] [Пинг/ID]** — перемещает пользователя по голосовым каналам.
**{pref}untroll** — выключение команды troll.
**{pref}reactions [Количество] [Эмодзи] [ID Канала]** — спамит реакциями.
**{pref}ball [Вопрос]** — ответит на любые вопросы.
**{pref}hack [Пинг/ID]** — взлом аккаунта.
**{pref}faketyping [Длительность в секундах] [ID Канала]** — печатает сообщение...
**{pref}reactionbot [Эмодзи] [ID Сервера]** — ставит реакции на все сообщения.
**{pref}say [Пинг/ID] [Текст]** — пишет сообщение от имени другого пользователя.
**{pref}criptext** — делает ваши сообщения очень страшними!!!
**{pref}color [rainbow/water/white]** — делает ваши сообщения красочными.
''')
	elif cat=='moderation':
		await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Moderation⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}ban [Пинг/ID] [Причина]** — банит пользователя.
**{pref}unban - [Пинг/ID]** — разбанивает пользователя.
**{pref}kick [Пинг/ID] [Причина]** — кикает пользователя.
**{pref}mute [Пинг/ID] [Длительность] [Причина]** — мутит пользователя.
**{pref}unmute [Пинг/ID] [Причина]** — размучивает пользователя.
**{pref}slowmode [Длительность]** — ставит слоумод на канал (Пример длительности: 3ч - 3 часа).
''')
	elif cat=='image':
		await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Image⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}lgbt [Пинг/ID]** — делает аватарку пользователя разноцветной.
**{pref}comment [Пинг/ID] [Текст]** — делает комментарий на ютубе.
**{pref}jail [Пинг/ID]** — садит пользователя в тюрьму.
**{pref}cmm [Текст]** — change my mind.
**{pref}fox** — картинка лисы.
**{pref}lightshot [Количество]** — генерирует случайные ссылки на lighshot.
**{pref}qrcode [Контент]** — создаёт QRcode.
''')
	elif cat=='nuke':
		if await check(ctx):
			await ctx.message.edit(content=f'''
⟃⟞⟞⟞⟞⟞⟞⟞✫**⟮Nuke⟯**✫⟝⟝⟝⟝⟝⟝⟝⟝⟄
**{pref}nuke** — уничтожение сервера.
**{pref}silentnuke [ID Сервера] [Сообщение]** — уничтожение сервера с обходом ВСЕХ анти-краш ботов, и нельзя определить, кто уничтожил сервер.
**{pref}spamchannels [Имя]** — спам каналами.
**{pref}spamroles [Имя]** — спам ролями.
**{pref}spamwebhooks [Сообщение]** — спам вебхуками.
**{pref}spam [Количество] [Текст]** — спам с обходом анти-спама.
**{pref}spamall [Количество] [Текст]** — спам во все каналы.
**{pref}spamthreads [Количество] [Имя ветки]** — спамит ветками.
**{pref}spamthreadsall [Количество] [Имя ветки]** — спамит во всех каналах ветками.
**{pref}spamgroups [Количество] [Жертвы от 2 до 9]** — спамит группами.
**{pref}pingall [Количество]** — пингует всех участников на сервере.
**{pref}lags [Тип лагов] [Количество]** — делает сильные лаги в канале.
**{pref}nukechannel** — удаляет все сообщения в канале, и меняет айди канала.
**{pref}deleteall** — удаление всего.
**{pref}deletechannels** — удаляет только каналы.
**{pref}deleteroles** — удаляет только роли.
**{pref}deleteemojis** — удаляет только эмодзи.
''')
	else:
		await ctx.message.edit(content=f'**__Selfbot__\n\n:x: Напишите `{pref}help` для просмотра всех категорий команд**')
@bot.command(name='bot', aliases=['selfbot', 'бот', 'селфбот'])
async def __bot(ctx):
	await ctx.message.edit(content='**__Selfbot__\n\nСсылка: https://github.com/PuroSlavKing/Discord-Selfbot **')
@bot.command(aliases=['перезагрузка', 'стоп', 'перезагрузить', 'stop_all', 'остановить', 'reload', 'stop', 'reset'])
async def stopall(ctx):
	await ctx.message.edit(content=f'''
Перезагрузка бота...
█▒▒▒▒▒▒▒▒▒
''')
	clear()
	Popen('python main.py')
	await ctx.message.edit(content=f'''
Перезагрузка завершена!
██████████
''')
	await bot.logout()
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")
try: bot.run(config['GENERAL']["token"])
except:
	while True:
		clear()
		print(Fore.LIGHTBLUE_EX+"Неверный токен")
		while True: sleep(9)
