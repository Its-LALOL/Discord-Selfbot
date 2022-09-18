import discord
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=['server', 'сервер', 'гильдия'])
	async def guild(self, ctx):
		bots=0
		users=0
		for user in ctx.guild.members:
			if user.bot:
				bots+=1
			else:
				users+=1
		mentions=0
		admins=0
		for role in ctx.guild.roles:
			if role.mentionable:
				mentions+=1
			if role.permissions.administrator:
				admins+=1
		owner=f'`{ctx.guild.owner}` - (`{ctx.guild.id}`)'
		if ctx.guild.owner is None:
			owner='`Unknown`'
		createdat=round(ctx.guild.created_at.timestamp())
		await ctx.message.edit(content=f'__**Selfbot by LALOL**__\n\n```Базовое```**Имя: `{ctx.guild.name}`\nID: `{ctx.guild.id}`\nСоздатель: {owner}\nСоздан: <t:{createdat}> (<t:{createdat}:R>)```Участники и боты [Информация может быть не точная]```Участников: `{users}`\nБотов: `{bots}`\nВсего: `{users+bots}` ```Каналы```Текстовых: `{len(ctx.guild.text_channels)}`\nГолосовых: `{len(ctx.guild.voice_channels)}`\nКатегорий: `{len(ctx.guild.categories)}`\nВсего: `{len(ctx.guild.channels)}` ```Роли```Пингующихся: `{mentions}`\nАдминских: `{admins}`\nВсего: `{len(ctx.guild.roles)}`**')
	@commands.command(aliases=['юзер', 'участник', 'member', 'инфо', 'информация', 'info', 'information'])
	async def user(self, ctx, user:discord.User=None):
		if user is None:
			user=ctx.author
		try:user1=ctx.guild.get_member(user.id)
		except:user1=None
		if user1 is None:
			bot='Нет'
			if user.bot:
				bot='Да'
			createdat=round(user.created_at.timestamp())
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nИмя: `{user.name}`\nТег: `{user.discriminator}`\nID: `{user.id}`\nБот: `{bot}`\nАккаунт создан: <t:{createdat}> (<t:{createdat}:R>)**')
		else:
			user=user1
			owner='Нет'
			if ctx.guild.owner==user:
				owner="Да"
			bot="Нет"
			if user.bot:
				bot="Да"
			createdat=round(user.created_at.timestamp())
			joinedat=round(user.joined_at.timestamp())
			if str(user.status)=='online':
				status='В сети'
			if str(user.status)=='idle':
				status='Неактивен'
			if str(user.status)=='dnd':
				status='Не беспокоить'
			if str(user.status)=='offline':
				status='Не в сети'
			if user.is_on_mobile():
				status=status+' (Телефон)'
			nick=''
			if not user.nick is None:
				nick=f'Ник: `{user.nick}`\n'
			voice=''
			if not user.voice is None:
				voice=f'Голосовой канал: {user.voice.channel.mention}\n'
			admin='Нет'
			if user.guild_permissions.administrator:
				admin='Да'
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nИмя: `{user.name}`\nТег: `{user.discriminator}`\nID: `{user.id}`\n{nick}Бот: `{bot}`\nСоздатель: `{owner}`\nАдмин: `{admin}`\nСамая высокая роль: `@{user.top_role.name}`\n{voice}Статус: `{status}`\nАккаунт создан: <t:{createdat}> (<t:{createdat}:R>)\nЗашёл на сервер: <t:{joinedat}> (<t:{joinedat}:R>)**')
def setup(bot):
	bot.add_cog(Info(bot))
