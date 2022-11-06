import discord
from discord.ext import commands
import random, string
from asyncio import sleep
import requests
from emoji import EMOJI_DATA
from colorama import Fore
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

troll={'server_id': 0, 'user_id': 0, 'mode': 0, 'emoji': None} # 1 - trolldelete, 2 - trollreaction, 3 - trollrepeat
reactionbot={'enabled': False, 'emoji': None, 'server_id': None}
text_mode=''

def crip(text): #оч страшна ваще
	message=''
	for i in text:
		i=i.lower()
		if i=='б': i='6'
		if i=='с': i='s'
		if i=='з': i='z'
		if i=='ч': i='4'
		if i=='и': i='u'
		if i=='п': i='n'
		if i=='в': i='v'
		if i=='т': i='t'
		if i=='й': i='j'
		if i=='д': i='d'
		if i=='к': i='k'
		if i=='м': i='m'
		if i=='о': i='0'
		message+=i
	return message
def to_color(text):
	output='```ansi\n'
	if text_mode=='rainbow':
		colors_bad=[Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA] # цвета радуги
	elif text_mode=='water':
		colors_bad=[Fore.CYAN, Fore.BLUE] # цвет вады!!!!!
	elif text_mode=='white':
		colors_bad=[Fore.WHITE] # чорныи
	else:
		return f'> {text}\n\n**__Selfbot by LALOL__\n\n:warning: Указан неправильный цвет!**'
	colors=[]
	for i in colors_bad: # кто украдёт команду тот самый худший человек!!! ну рил без рофлов
		color=i.replace('\x1b', '').replace('[', '')
		colors.append(color)
	minus=0
	count=0
	for i in text: # 20 минут сидел мучался с этой штукой
		if i==' ': # если пробел
			output+=i
			continue
		try: to_add=f'[2;{colors[count-minus]}{i}'
		except:
			minus=count
			to_add=f'[2;{colors[count-minus]}{i}'
		output+=to_add
		count+=1
	output+='\n```'
	return output
class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def trolldelete(self, ctx, *, user:discord.Member):
		await ctx.message.delete()
		global troll
		troll['server_id']=ctx.guild.id
		troll['user_id']=user.id
		troll['mode']=1
	@commands.command(aliases=['trollreactions'])
	async def trollreaction(self, ctx, user:discord.User, emoji='🤡'):
		await ctx.message.delete()
		global troll
		troll['server_id']=-1
		troll['user_id']=user.id
		troll['emoji']=emoji
		troll['mode']=2
	@commands.command()
	async def trollrepeat(self, ctx, user:discord.User):
		await ctx.message.delete()
		global troll
		troll['server_id']=-1
		troll['user_id']=user.id
		troll['mode']=3
	@commands.command()
	async def trollmove(self, ctx, amount:int, *, user:discord.Member):
		await ctx.message.delete()
		channels=ctx.guild.voice_channels
		lastchannel=None
		if len(channels) in [0, 1]: return
		for i in range(amount):
			while True:
				channel=random.choice(channels)
				if channel!=lastchannel:
					await user.move_to(channel)
					lastchannel=channel
					break
		await ctx.send(f"**__Selfbot by LALOL__\n\n:nauseated_face: Успешно переместил `{user}` {amount} раз!**")
	@commands.command()
	async def untroll(self, ctx):
		await ctx.message.delete()
		global troll
		troll['user_id']=0
	@commands.Cog.listener()
	async def on_message(self, message):
		global text_mode
		if message.author.id==self.bot.user.id and not message.content.startswith(config['GENERAL']['prefix']) and not 'Selfbot by LALOL' in message.content:
			global text_mode
			if text_mode=='crippytext':
				await message.edit(content=crip(message.content))
			elif text_mode!='':
				await message.edit(content=to_color(message.content))
		try:
			if troll['mode'] in [2, 3]:
				if message.author.id==troll['user_id']:
					if troll['mode']==2: await message.add_reaction(troll['emoji'])
					if troll['mode']==3:
						text=message.content.replace('@', '')
						if message.content.startswith(config['Prefix']):
							text=message.content.replace(config['Prefix'], '', )
						await message.reply(text)
			else:
				if message.guild.id: return
				if message.author.id==troll['user_id'] and message.guild.id==troll['server_id']: await message.delete()
		except:pass
		global reactionbot
		if reactionbot['enabled'] and message.guild.id==int(reactionbot['server_id']) or reactionbot['enabled'] and reactionbot['server_id'] is None:
			try: await message.add_reaction(reactionbot['emoji'])
			except: pass
	@commands.command(aliases=['react', 'reaction', 'реакция', 'реакции', 'reactionall'])
	async def reactions(self, ctx, amount: int=15, emoji='🤡', channel_id: int=None):
		await ctx.message.delete()
		if channel_id is None: channel=ctx.channel
		else: channel=self.bot.get_channel(channel_id)
		messages=await channel.history(limit=amount).flatten()
		reactioned=0
		for message in messages:
			await message.add_reaction(emoji)
			reactioned+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:stuck_out_tongue_winking_eye: Успешно поставил {reactioned} реакций!**")
	@commands.command(aliases=['lag', 'лаг', 'лаги', 'ascii'])
	async def lags(self, ctx, cat='ы', amount: int=15):
		await ctx.message.delete()
		if cat=='random':
			for i in range(amount):
				text=''
				for i in range(2000):
					text=text+chr(random.randrange(1114111))
				await ctx.send(content=text)
		elif cat=='chains':
			text=":chains:"*199
			for i in range(amount):
				char=random.choice(string.digits+string.ascii_letters)
				await ctx.send(text+char)
		elif cat=='phone':
			for i in range(amount):
				char=random.choice(string.digits+string.ascii_letters)
				await ctx.send('О̶̿̏҉͛͑́҉̑͋́҉͐̋͋҉́̌̒҈̀͊̏҉̈́͋́҉̃̎͊҈͛̆̀҉̔̿͋҈̾͒͒҈̀̋̉҉̍̂́҈̃̒̔҈͑̂́҈̉̑̈́҉̌̐́ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О̶̿̏҉͛͑́҉̑͋́҉͐̋͋҉́̌̒҈̀͊̏҉̈́͋́҉̃̎͊҈͛̆̀҉̔̿͋҈̾͒͒҈̀̋̉҉̍̂́҈̃̒̔҈͑̂́҈̉̑̈́҉̌̐́ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О̶̿̏҉͛͑́҉̑͋́҉͐̋͋҉́̌̒҈̀͊̏҉̈́͋́҉̃̎͊҈͛̆̀҉̔̿͋҈̾͒͒҈̀̋̉҉̍̂́҈̃̒̔҈ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰  ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰О҉҉҉҉҈҉҉҈҉҈҈҉҈ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰О̶̿̏҉͛͑҉҉҉҈҉҉҈҉҈҈҉҈҈҈҉ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰ ꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟'+char)
		elif cat=='emojis':
			emojisdata=EMOJI_DATA
			emojis=[]
			for i in emojisdata:
				emojis.append(i[0])
			for i in range(amount):
				text=''
				for i in range(1000):
					try: text+=random.choice(emojis)
					except: pass
				await ctx.send(text)
		else:
			await ctx.send(content="**__Selfbot by LALOL__\n\n:chains:`chains` - Спамит цепями (Лагает на слабых пк)\n:ideograph_advantage:`random` - Спамит случайными символами (Лагает на слабых пк и на телефонах +в дискорде во время спама проиходят баги)\n:mobile_phone:`phone` - Спамит лагающими символами (Очень сильно лагает на телефонах)\n:smiley:`emojis` - Спамит эмодзями (Очень сильно лагает на слабых пк и на телефонах)**")
			return
		await ctx.send(f"**__Selfbot by LALOL__\n\n:brain: Успешно отправил {amount} лагающих сообщений!**")
	@commands.command(aliases=['шар'])
	async def ball(self, ctx, *, text):
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n> {text}\n:crystal_ball: Шар думает...**')
		await sleep(random.uniform(1, 5))
		answer=random.choice(['Конечно!', 'Нет', 'Да', 'Не знаю', 'Сомневаюсь', 'Очевидно, что ответ будет да', 'Очевидно, что ответ будет нет'])
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n> {text}\n:crystal_ball: Шар отвечает: `{answer}`**')
	@commands.command(aliases=['взлом', 'взломать'])
	async def hack(self, ctx, *, victim:discord.User):
		fulltoken=requests.get(f'https://some-random-api.ml/bottoken?id={victim.id}').json()['token']
		token=''
		number=4
		for i in fulltoken:
			token+=i
			number+=1
			if number>4:
				number=0
				unk=''
				for i in range(len(fulltoken)-len(token)):
					unk+='_'
				await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n> Получение токена `{victim}`...\n`{token}{unk}`**')
				await sleep(1)
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nЗахожу в аккаунт `{victim}`...**')
		await sleep(5)
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:rat: Успешно зашёл в аккаунт `{victim}`**')
	@commands.command(aliases=['сказать'])
	async def say(self, ctx, victim:discord.User, *, text):
		await ctx.message.delete()
		name=victim.name
		try:name=victim.nick
		except:pass
		while True:
			for webhook in await ctx.channel.webhooks():
				try: await webhook.send(text, username=name, avatar_url=victim.avatar_url)
				except: continue
				return
			webhook=await ctx.channel.create_webhook(name='Selfbot by LALOL')
	@commands.command(aliases=['fake_type', 'фейк_печать','фейкпечать', 'faketype'])
	async def faketyping(self, ctx, seconds:int, channel_id: int=None):
		await ctx.message.delete()
		if channel_id is None: channel=ctx.channel
		else: channel=self.bot.get_channel(channel_id)
		async with channel.typing():
			await sleep(seconds)
	@commands.command(name='reactionbot', aliases=['reaction_bot'])
	async def __reactionbot(self, ctx, emoji='🤡', server_id=None):
		global reactionbot
		if reactionbot['enabled']:
			reactionbot['enabled']=False
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\n:red_circle: Reaction Bot был успешно выключен!**")
		else:
			reactionbot['enabled']=True
			reactionbot['emoji']=emoji
			reactionbot['server_id']=server_id
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\n:green_circle: Reaction Bot был успешно включён!**")
	@commands.command(aliases=['crippytext', 'textcrippy', 'textcrip'])
	async def criptext(self, ctx, *, text=None):
		message=''
		if text is None:
			global text_mode
			if text_mode=='crippytext':
				text_mode=''
				await ctx.message.edit(content="**__Selfbot by LALOL__\n\n:red_circle: crippytext был успешно выключён!**")
				return
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\n:green_circle: crippytext был успешно включен!**")
			text_mode='crippytext'
			return
		await ctx.message.edit(content=crip(text))
	@commands.command(aliases=['цвет', 'colour'])
	async def color(self, ctx, *, color='rainbow', text=None):
		message=''
		color=color.lower()
		if text is None:
			global text_mode
			if text_mode==color:
				text_mode=''
				await ctx.message.edit(content=f"**__Selfbot by LALOL__\n\n:red_circle: {color} был успешно выключён!**")
				return
			await ctx.message.edit(content=f"**__Selfbot by LALOL__\n\n:green_circle: {color} был успешно включен!**")
			text_mode=color
			return
		await ctx.message.edit(content=to_color(text))
def setup(bot):
	bot.add_cog(Fun(bot))
