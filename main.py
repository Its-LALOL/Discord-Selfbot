import os
try:
	import discord
	from discord.ext import commands
	from colorama import init, Fore;init()
	import requests
except:
	os.system('pip install -U discord.py-self colorama requests')
	import discord
	from discord.ext import commands
	from colorama import init, Fore;init()
	import requests
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)
version=1.0
Intro=Fore.RED +"""
██╗░░░░░░█████╗░██╗░░░░░░█████╗░██╗░░░░░
██║░░░░░██╔══██╗██║░░░░░██╔══██╗██║░░░░░
██║░░░░░███████║██║░░░░░██║░░██║██║░░░░░
██║░░░░░██╔══██║██║░░░░░██║░░██║██║░░░░░
███████╗██║░░██║███████╗╚█████╔╝███████╗
╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░╚══════╝\n
"""+Fore.GREEN + "Selfbot by LALOL\n" + Fore.RED
clear=lambda: os.system(f'cls && title Selfbot by LALOL {version}' if os.name == 'nt' else 'clear')
clear()
print(Intro)
pref=config['Prefix']
bot=commands.Bot(command_prefix=pref, case_insensitive=True, self_bot=True)
bot.remove_command('help')
update=''

async def check(ctx):
	if not config['nuke_commands']:
		await ctx.message.edit(content='**__Selfbot by LALOL__\n\n:warning: Краш команды отключены! Для того чтобы включить краш команды измените файл config.json**')
		return False
	return True

@bot.event
async def on_connect():
	for filename in os.listdir():
		if filename.endswith('.txt'):
			os.remove(filename)
	status=config['Status']
	sstatus=discord.Status.online
	if status=='idle':
		sstatus=discord.Status.idle
	if status=='dnd':
		sstatus=discord.Status.dnd
	if status=='invisible':
		sstatus=discord.Status.invisible
	await bot.change_presence(status=sstatus)
	print(Fore.MAGENTA + f"Аккаунт: {Fore.YELLOW}{bot.user}{Fore.MAGENTA}\nID: {Fore.YELLOW}{bot.user.id}{Fore.MAGENTA}\nPrefix: {Fore.YELLOW}{pref}")
	if float(requests.get('https://raw.githubusercontent.com/Its-LALOL/Discord-Selfbot/main/cogs/version').text)>version:
		global update
		update=f':warning: Пожалуйста обновите селфбота используя команду {pref}bot**\n**'
		print(f'{Fore.CYAN}Пожалуйста обновите селфбота используя команду {pref}bot{Fore.RED}\n')
		return
	print(Fore.RED)
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		error='Недостаточно аргументов!'
	elif isinstance(error, commands.CommandNotFound):
		return
	elif isinstance(error, commands.BadArgument):
		error='Указан не правильный аргумент!'
#	elif isinstance(error, commands.Forbidden):
#		error='Не достаточно прав для выполнения данной команды!'
	print(f"{Fore.RED}[ERROR] {error}")
	try: await ctx.send(f'**__Selfbot by LALOL__\n\nПроизошла ошибка :x:\n```{error}```**')
	except: pass
@bot.command(aliases=['хелп', 'помощь'])
async def help(ctx, cat=None):
	if cat==None:
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:screwdriver:`{pref}help Tools` - Полезные команды\n:information_source:`{pref}help Info` - Команды для получения информации\n:joy:`{pref}help Fun` - Развлекательные команды\n:shield:`{pref}help Moderation` - Команды модерации\n:boom:`{pref}help Nuke` - Команды краша\n\n:robot:`{pref}bot` - Получение ссылки на установку селф бота**')
		return
	cat=cat.lower()
	if cat=='tools':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:comet:`{pref}status [Тип статуса] [Текст]` - Меняет статус\n:broom:`{pref}purge [Количество]` - Удаляет ваши сообщения\n:pushpin:`{pref}masspin [Количество]` - Закрепляет сообщения\n:speaking_head:`{pref}spam [Количество] [Текст]` - Спам с обходом анти-спама\n:eye:`{pref}pingall` - Пингует всех участников на сервере\n:envelope:`{pref}messages [Количество]` - Сохраняет сообщения в файл**')
	elif cat=='info':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:pen_fountain:`{pref}server` - Информация о сервере\n:pen_ballpoint:`{pref}user [ID/Пинг]` - Информация об аккаунте**')
	elif cat=='fun':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:face_with_symbols_over_mouth:`{pref}trolldelete [ID/Пинг]` - Удаление всех сообщений пользователя\n:imp:`{pref}trollreaction [ID/Пинг] [Эмодзи]` - Ставка реакций на все сообщения пользователя\n:ghost:`{pref}trollrepeat [ID/Пинг]` - Повторение всех сообщений пользователя\n:slight_smile:`{pref}untroll` - Выключение команды troll\n:stuck_out_tongue_winking_eye:`{pref}reactions [Количество] [Эмодзи]` - Спамит реакциями\n:brain:`{pref}lags [Тип лагов] [Количество]` - Делает очень сильные лаги в канале\n:crystal_ball:`{pref}ball [Вопрос]` - Ответит на любые (почти) вопросы\n:rat:`{pref}hack [Пинг/ID]` - Фейковый взлом аккаунта**')
	elif cat=='moderation':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:dagger:`{pref}ban [Пинг/ID] [Причина]` - Банит пользователя\n:ok_hand:`{pref}unban - [Пинг/ID]` - Разбанивает пользователя\n:door:`{pref}kick [Пинг/ID] [Причина]` - Кикает участника\n:mute:`{pref}mute [Пинг/ID] [Длительность] [Причина]` - Мутит участника\n:sound:`{pref}unmute [Пинг/ID] [Причина]` - Размучивает участника\n:timer:`{pref}slowmode [Длительность]` - Ставит слоумод на канал (Пример длительности: 3ч - 3 часа)**')
	elif cat=='nuke':
		if await check(ctx):
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:skull:`{pref}nuke` - Уничтожение сервера\n:smiling_imp:`{pref}spamchannels [Имя]` - Спам каналами\n:jack_o_lantern:`{pref}spamroles [Имя]` - Спам ролями\n:cold_face:`{pref}spamwebhooks [Сообщение]` - Спам вебхуками\n:clown:`{pref}deleteall` - Удаление всего\n\n`{pref}deletechannels` - Удаляет каналы\n`{pref}deleteroles` - Удаляет роли\n`{pref}deleteemojis` - Удаляет эмодзи**')
	else:
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Напишите `{pref}help` для просмотра всех категорий команд**')
@bot.command(name='bot', aliases=['selfbot', 'бот', 'селфбот'])
async def __bot(ctx):
	await ctx.message.edit(content='**__Selfbot by LALOL__\n\nСсылка: https://github.com/Its-LALOL/Discord-Selfbot**')
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")
try: bot.run(config["Token"])
except:
	while True:
		input("Invalid Token!")
