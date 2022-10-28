import discord
from discord.ext import commands
import requests
import datetime
from urllib.parse import quote

class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['бан', 'забанить'])
	async def ban(self, ctx, user:discord.User, *, reason='Причина не указана'):
		try: await ctx.guild.ban(user, reason=reason)
		except:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Не удалось забанить пользователя `{user}`**')
			return
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:dagger: Пользователь `{user}` успешно был забанен по причине `{reason}`**')
	@commands.command(aliases=['разбанить', 'разбан'])
	async def unban(self, ctx, user:discord.User):
		try: await ctx.guild.unban(user)
		except:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Не удалось разбанить пользователя `{user}`**')
			return
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:ok_hand: Пользователь `{user}` успешно был разбанен**')
	@commands.command(aliases=['кик', 'выгнать', 'кикнуть'])
	async def kick(self, ctx, user:discord.Member, *, reason='Причина не указана'):
		try: await ctx.guild.kick(user, reason=reason)
		except:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Не удалось кикнуть пользователя `{user}`**')
			return
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:door: Пользователь `{user}` успешно был кикнут по причине `{reason}`**')
	@commands.command(aliases=['мут', 'мьют', 'замутить', 'замьютить'])
	async def mute(self, ctx, user:discord.Member, time, *, reason='Причина не указана'):
		if time.endswith('s') or time.endswith('с'):
			timeout=(datetime.datetime.utcnow()+datetime.timedelta(seconds=int(time.replace('s', '').replace('с', '')))).isoformat()
		elif time.endswith('m') or time.endswith('м'):
			timeout=(datetime.datetime.utcnow()+datetime.timedelta(minutes=int(time.replace('m', '').replace('м', '')))).isoformat()
		elif time.endswith('h') or time.endswith('ч'):
			timeout=(datetime.datetime.utcnow()+datetime.timedelta(hours=int(time.replace('h', '').replace('ч', '')))).isoformat()
		elif time.endswith('d') or time.endswith('д'):
			timeout=(datetime.datetime.utcnow()+datetime.timedelta(days=int(time.replace('d', '').replace('д', '')))).isoformat()
		else:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Вы неправильно указали длительность мута!**')
			return
		response=requests.patch(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', headers={"Authorization": self.bot.http.token, 'X-Audit-Log-Reason': quote(reason)}, json={"communication_disabled_until": timeout})
		if response==403:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Не удалось замутить пользователя `{user}`**')
			return
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:mute: Пользователь `{user}` был успешно замучен по причине `{reason}` на `{time}`**')
	@commands.command(aliases=['размут', 'размьют', 'размутить', 'размьютить'])
	async def unmute(self, ctx, user:discord.Member, *, reason='Причина не указана'):
		response=requests.patch(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', headers={"Authorization": self.bot.http.token, 'X-Audit-Log-Reason': quote(reason)}, json={"communication_disabled_until": 0})
		if response==403:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Не удалось размутить пользователя `{user}`**')
			return
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:sound: Пользователь `{user}` был успешно размучен по причине `{reason}`**')
	@commands.command(alises=['слоумод'])
	async def slowmode(self, ctx, time):
		if time.endswith('s') or time.endswith('с'):
			seconds=int(time.replace('s', '').replace('с', ''))
		elif time.endswith('m') or time.endswith('м'):
			seconds=int(time.replace('m', '').replace('м', ''))*60
		elif time.endswith('h') or time.endswith('ч'):
			seconds=int(time.replace('h', '').replace('ч', ''))*60*60
		else:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Длительность слоумода указана неправильно!**')
			return
		if seconds>21600:
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Слоумод не может быть больше 6 часов!**')
			return
		await ctx.channel.edit(slowmode_delay=seconds)
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:timer: Слоумод канала был успешно изменён на {seconds} секунд**')
	@commands.command(alises=['channelnuke', 'nuke_channel', 'channel_nuke'])
	async def nukechannel(self, ctx):
		new_channel=await ctx.channel.clone()
		await new_channel.edit(category=ctx.channel.category, position=ctx.channel.position)
		await ctx.channel.delete()
def setup(bot):
	bot.add_cog(Moderation(bot))
