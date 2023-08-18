import discord
from discord.ext import commands
from asyncio import sleep
import requests
import random, string
from googletrans import Translator
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	config = json.load(f)

@commands.command(pass_context=True, name="eval")
async def _eval(self, ctx, *, body: str):
	"""Evaluates python code"""
	env = {
		"client": self.client,
		"ctx": ctx,
		"channel": ctx.channel,
		"author": ctx.author,
		"guild": ctx.guild,
		"message": ctx.message,
		"_": self._last_result,
		"source": inspect.getsource,
	}

class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['статус', 'activity', 'активность'])
	async def status(self, ctx, cat='ы', *, name='Selfbot'):
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
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.playing, application_id=1029430390357774388, name='Discord', assets={'large_image': '1029438970666426408', 'large_text': 'github.com/PuroSlavKing/Discord-Selfbot'}))
		elif cat in selfbot:
			await self.bot.change_presence(status=sstatus, activity=discord.Activity(type=discord.ActivityType.playing, application_id=1032671485120229397, name='Selfbot', details='github.com/PuroSlavKing/Discord-Selfbot', assets={'large_image': '1032672678106116216', 'large_text': 'github.com/PuroSlavKing/Discord-Selfbot'}))
		else:
			await ctx.message.edit(content="**Доступные варианты: ```Обычные````Watching`, `Listening`, `Playing`, `Streaming` и `Reset`\n\n```Эксклюзивные````Discord`, `Selfbot`**")
			return
		await ctx.message.edit(content='**:comet: Ваш статус был успешно изменён!**')
	@commands.command(alises=['clean', 'очистка', 'очистить'])
	async def purge(self, ctx, amount: int):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		deleted=0
		for message in messages:
			if message.author.id==self.bot.user.id:
				await message.delete()
				deleted+=1
		await ctx.send(f"**:broom: Успешно удалил {deleted} сообщений!**")
	@commands.command()
	async def clear(self, ctx, amount: int = 100):
		await ctx.message.delete()
		deleted = 0
		async for message in ctx.channel.history(limit=amount):
			await message.delete()
			deleted += 1
		await ctx.send(f"**:broom: Успешно удалил {deleted} сообщений!**")
	@commands.command(aliases=['spampin', 'pinspam', 'pinmass', 'pin', 'закрепить'])
	async def masspin(self, ctx, amount: int=15):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		pinned=0
		for message in messages:
			try: await message.pin()
			except: pass
			pinned+=1
		await ctx.send(f"**:pushpin: Успешно закрепил {pinned} сообщений!**")
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
		await ctx.send(f"**:envelope: Успешно сохранил {saved} сообщений!**", file=discord.File(f'messages_{ctx.channel.id}.txt'))
	@commands.command(aliases=['leavegroups', 'leavegroup', 'groupleave'])
	async def groupsleave(self, ctx):
		await ctx.message.delete()
		leaved=0
		for group in self.bot.private_channels:
			if not 'Direct Message' in str(group) and not str(group).lower()=='избранное': 
					await group.leave()
					leaved+=1
		await ctx.send(f"**:busts_in_silhouette: Успешно вышел из {leaved} групп!**")
	@commands.command(aliases=['block_send'])
	async def blocksend(self, ctx, user:discord.User, *, text):
		await user.unblock()
		await user.send(text)
		await user.block()
		await ctx.message.delete()
	@commands.command(aliases=['copy_status', 'copyactivity', 'copy_activity', 'statuscopy', 'status_copy', 'activitycopy', 'activity_copy'])
	async def copystatus(self, ctx, user:discord.Member):
		await self.bot.change_presence(activity=user.activity)
		await ctx.message.edit(content=f"**:jigsaw: Успешно скопировал статус у `{user}`!**")
	@commands.command(aliases=['translation', 'переводчик', 'перевести', 'trans'])
	async def translate(self, ctx, to='ru', *, text=None):
		if text is None:
			if not ctx.message.reference:
				await ctx.reply(f"**:warning: Для того чтобы перевести ответьте на сообщение или напишите текст!**")
				return
			message=await ctx.channel.fetch_message(ctx.message.reference.message_id)
			text=message.content
		translator=Translator()
		translation=translator.translate(text, dest=to)
		src=translation.src
		if src=='en': src='gb'
		dest=translation.dest
		if dest=='en': dest='gb'
		await ctx.message.edit(content=f'**:flag_{src}:: `{text}`\n:flag_{dest}:: `{translation.text}`**')
	@commands.command()
	async def nitro(self, ctx, amount: int=100_000, nitrotype='classic'):
		await ctx.message.edit(content=f'**Генерирую {amount} нитро кодов...**')
		with open(f'{amount}_nitro_codes.txt', 'w', encoding='utf-8') as f:
			f.write('\n--------------------------------------------\n')
			count=24
			if nitrotype=='classic': count=16
			for i in range(amount):
				code=''.join(random.choices(string.ascii_letters+string.digits, k=count))
				f.write(f'discord.gift/{code}\n')
			f.write('--------------------------------------------')
		await ctx.send(f'**:crown: Успешно сгенерировал {amount} нитро кодов!**',file=discord.File(f'{amount}_nitro_codes.txt'))
		await ctx.message.delete()
	@commands.command(aliases=['copy_emojis', 'copy_emoji', 'copyemoji'])
	async def copyemojis(self, ctx, to_clone: int):
		await ctx.message.delete()
		guild=self.bot.get_guild(to_clone)
		for emoji in ctx.guild.emojis:
			content=requests.get(emoji.url).content
			await guild.create_custom_emoji(name=emoji.name, image=content)
		await ctx.send(f"**:smiley: Успешно скопировал все эмодзи!**")
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
		await ctx.send(f"**:hamsa: Успешно удалил {removed} лс!**")
def setup(bot):
	bot.add_cog(Tools(bot))
