import discord
from discord.ext import commands
from asyncio import sleep
import requests
import random, string
from googletrans import Translator
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['статус', 'activity', 'активность'])
	async def status(self, ctx, cat='ы', *, name='Selfbot by LALOL'):
		response=requests.get('https://discord.com/api/users/@me/settings', headers={'authorization': self.bot.http.token})
		status=response.json()['status']
		sstatus=discord.Status.online
		if status=='idle':
			sstatus=discord.Status.idle
		if status=='dnd':
			sstatus=discord.Status.dnd
		if status=='invisible':
			sstatus=discord.Status.invisible
		cat=cat.lower()
		discordd=['discord', 'дискорд']
		selfbot=['selfbot', 'селфбот']
		game=['play', 'playing', 'играть', 'играет', 'game', 'игра', 'играю']
		watching=['watching', 'watch', 'смотреть', 'смотрит', 'смотрю']
		listening=['listening', 'listen', 'слушает', 'слушать', 'слушаю']
		streaming=['streaming', 'stream', 'стрим', 'стримить', 'стримлю', 'стримит']
		reset=['reset', 'remove', 'none', 'off', 'убрать', 'выключить', 'обычный', 'ресет', 'delete', 'удалить']
		if cat in game:
			await self.bot.change_presence(status=sstatus, activity=discord.Game(name=name))
		elif cat in watching:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.watching, name=name))
		elif cat in listening:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.listening, name=name))
		elif cat in streaming:
			await self.bot.change_presence(status=sstatus, activity=discord.Streaming(name=name, url="https://www.youtube.com/watch?v=yNIQi6cbk2s"))
		elif cat in reset:
			await self.bot.change_presence(status=sstatus, activity=None)
		elif cat in discordd:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.playing, application_id=1029430390357774388, name='Discord', assets={'large_image': '1029438970666426408', 'large_text': 'Selfbot by LALOL\nbit.ly/3CXNRpC'}))
		elif cat in selfbot:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.playing, application_id=1032671485120229397, name='Selfbot by LALOL', details='bit.ly/3CXNRpC', assets={'large_image': '1032672678106116216', 'large_text': 'Selfbot by LALOL\nbit.ly/3CXNRpC'}))
		else:
			await ctx.message.edit(content="**__Selfbot by LALOL__\n\nДоступные варианты: ```Обычные````Watching`, `Listening`, `Playing`, `Streaming` и `Reset`\n\n```Эксклюзивные````Discord`, `Selfbot`**")
			return
		await ctx.message.edit(content='**__Selfbot by LALOL__\n\n:comet: Ваш статус был успешно изменён!**')
	@commands.command(alises=['clean', 'clear', 'очистка', 'очистить'])
	async def purge(self, ctx, amount: int):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		deleted=0
		for message in messages:
			if message.author.id==self.bot.user.id:
				await message.delete()
				deleted+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:broom: Успешно удалил {deleted} сообщений!**")
	@commands.command(aliases=['spampin', 'pinspam', 'pinmass', 'pin', 'закрепить'])
	async def masspin(self, ctx, amount: int=15):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		pinned=0
		for message in messages:
			try: await message.pin()
			except: pass
			pinned+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:pushpin: Успешно закрепил {pinned} сообщений!**")
	@commands.command(aliases=['спам', 'flood', 'флуд'])
	async def spam(self, ctx, amount: int, *, text):
		await ctx.message.delete()
		for i in range(amount):
			await ctx.send(f'{text} ||{"".join(random.choices(string.ascii_uppercase+string.digits+string.ascii_lowercase, k=8))}||')
		await ctx.send(f"**__Selfbot by LALOL__\n\n:speaking_head: Успешно отправил {amount} сообщений!**")
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
		await ctx.send(f"**__Selfbot by LALOL__\n\n:eye: Успешно пинганул {pinged} пользователей {amount} раз!**")
	@commands.command(aliases=['copy', 'сообщения', 'сохранить'])
	async def messages(self, ctx, amount: int=30):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		messages.reverse()
		saved=0
		with open(f'messages_{ctx.channel.id}.txt', 'w', encoding='utf-8') as f:
			for message in messages:
				f.write(f'[{message.author}]: {message.content}\n')
				saved+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:envelope: Успешно сохранил {saved} сообщений!**", file=discord.File(f'messages_{ctx.channel.id}.txt'))
	@commands.command(aliases=['leavegroups', 'leavegroup', 'groupleave'])
	async def groupsleave(self, ctx):
		await ctx.message.delete()
		leaved=0
		for group in self.bot.private_channels:
			if not 'Direct Message' in str(group) and not str(group).lower()=='избранное': 
					await group.leave()
					leaved+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:busts_in_silhouette: Успешно вышел из {leaved} групп!**")
	@commands.command(aliases=['floodall', 'спамалл', 'флудалл'])
	async def spamall(self, ctx, amount: int, *, text):
		await ctx.message.delete()
		for i in range(amount):
			for channel in ctx.guild.text_channels:
				try: await channel.send(f'{text} ||{"".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))}||')
				except: pass
		await ctx.send(f"**__Selfbot by LALOL__\n\n:anger_right: Успешно отправил по {amount} сообщений в каждый канал!**")
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
					await ctx.send(f"**__Selfbot by LALOL__\n\nПроизошла ошибка :x:\n```Код ошибки: {response.status_code}\n{response.text}```**")
					return
		await ctx.send(f"**__Selfbot by LALOL__\n\n:thread: Успешно создал {amount} веток!**")
	@commands.command(aliases=['block_send'])
	async def blocksend(self, ctx, user:discord.User, *, text):
		await user.unblock()
		await user.send(text)
		await user.block()
		await ctx.message.delete()
	@commands.command(aliases=['groupspam', 'groupsspam'])
	async def spamgroups(self, ctx, amount: int, *, victims_list):
		await ctx.message.delete()
		victims_ids=victims_list.split(' ')
		for i in range(amount):
			while True:
				response=requests.post('https://discord.com/api/v9/users/@me/channels', headers={'authorization': self.bot.http.token}, json={'recipients': victims_ids})
				if response.status_code==200 or response.status_code==201:
					id=response.json()['id']
					requests.post(f"https://discord.com/api/v9/channels/{id}/messages", headers={'authorization': self.bot.http.token}, json={"content": "||@everyone|| **__Selfbot by LALOL\nhttps://github.com/Its-LALOL/Discord-Selfbot __**"})
					break
				elif response.status_code==429:
					seconds=response.json()['retry_after']
					if 100>seconds:
						await sleep(seconds)
				else:
					await ctx.send(content=f"**__Selfbot by LALOL__\n\nПроизошла ошибка :x:\n```Код ошибки: {response.status_code}\n{response.text}```**")
					return
		await ctx.send(content=f"**__Selfbot by LALOL__\n\n:bubbles: Успешно создал {amount} групп!**")
	@commands.command(aliases=['copy_status', 'copyactivity', 'copy_activity', 'statuscopy', 'status_copy', 'activitycopy', 'activity_copy'])
	async def copystatus(self, ctx, user:discord.Member):
		await self.bot.change_presence(activity=user.activity)
		await ctx.message.edit(content=f"**__Selfbot by LALOL__\n\n:jigsaw: Успешно скопировал статус у `{user}`!**")
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
						await ctx.send(f"**__Selfbot by LALOL__\n\nПроизошла ошибка :x:\n```Код ошибки: {response.status_code}\n{response.text}```**")
						return
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_flower: Успешно создал по {amount} веток в каждый канал!**")
	@commands.command(aliases=['translation', 'переводчик', 'перевести', 'trans'])
	async def translate(self, ctx, to='ru', *, text=None):
		if text is None:
			if not ctx.message.reference:
				await ctx.reply(f"**__Selfbot by LALOL__\n\n:warning: Для того чтобы перевести ответьте на сообщение или напишите текст!**")
				return
			message=await ctx.channel.fetch_message(ctx.message.reference.message_id)
			text=message.content
		translator=Translator()
		translation=translator.translate(text, dest=to)
		src=translation.src
		if src=='en': src='gb'
		dest=translation.dest
		if dest=='en': dest='gb'
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:flag_{src}:: `{text}`\n:flag_{dest}:: `{translation.text}`**')
	@commands.command()
	async def nitro(self, ctx, amount: int=100_000, nitrotype='classic'):
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nГенерирую {amount} нитро кодов...**')
		with open(f'{amount}_nitro_codes.txt', 'w', encoding='utf-8') as f:
			f.write('Selfbot by LALOL\nhttps://github.com/Its-LALOL/Discord-Selfbot\n--------------------------------------------\n')
			count=24
			if nitrotype=='classic': count=16
			for i in range(amount):
				code=''.join(random.choices(string.ascii_letters+string.digits, k=count))
				f.write(f'discord.gift/{code}\n')
			f.write('--------------------------------------------\nSelfbot by LALOL\nhttps://github.com/Its-LALOL/Discord-Selfbot')
		await ctx.send(f'**__Selfbot by LALOL__\n\n:crown: Успешно сгенерировал {amount} нитро кодов!**',file=discord.File(f'{amount}_nitro_codes.txt'))
		await ctx.message.delete()
	@commands.command(aliases=['copy_emojis', 'copy_emoji', 'copyemoji'])
	async def copyemojis(self, ctx, to_clone: int):
		await ctx.message.delete()
		guild=self.bot.get_guild(to_clone)
		for emoji in ctx.guild.emojis:
			content=requests.get(emoji.url).content
			await guild.create_custom_emoji(name=emoji.name, image=content)
		await ctx.send(f"**__Selfbot by LALOL__\n\n:smiley: Успешно скопировал все эмодзи!**")
	@commands.command(aliases=['hackclean', 'hackclear'])
	async def hackpurge(self, ctx):
		await ctx.send("⠀" + "\n"*1998 + "⠀")
		await ctx.message.delete()
	@commands.command(aliases=['delete_dms', 'delete-dms', 'deletedm', 'delete-dm', 'delete_dm'])
	async def deletedms(self, ctx, name='spam'):
		await ctx.message.delete()
		removed=0
		for dm in self.bot.private_channels:
			if name.lower() in str(dm).lower():
				while True:
					response=requests.delete(f"https://discord.com/api/v9/channels/{dm.id}", headers={'authorization': self.bot.http.token})
					if response!=401: break
					sleep(response.json()['retry_after'])
				removed+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:hamsa: Успешно удалил {removed} лс!**")
def setup(bot):
	bot.add_cog(Tools(bot))
