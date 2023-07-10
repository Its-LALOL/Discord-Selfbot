import discord
from discord.ext import commands
import requests

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
		await ctx.message.edit(content=f"""
 📑 〢**Информация о сервере:**
 ├ 🆔・**Название сервера:** `{ctx.guild.name}`
 ├ 🆔・**ID Сервера:** `{ctx.guild.id}`
 └ 🕒・**Дата и время создания сервера:** <t:{createdat}> (<t:{createdat}:R>)
 #️⃣ 〢**Каналы:**
 ├ 📚・**Всего:** `{len(ctx.guild.channels)}`
 ├ 💬・**Текстовых:** `{len(ctx.guild.text_channels)}`
 ├ 🔊・**Голосовых:** `{len(ctx.guild.voice_channels)}`
 └ 📂・**Категорий:** `{len(ctx.guild.categories)}`
 🏴 〢**Роли:**
 ├ 📚・**Всего:** `{len(ctx.guild.roles)}`
 ├ 📚・**Пингующихся:** `{mentions}`
 └ 🔨・**С правами администратора:** `{admins}`
 👥 〢**Участники:**
 ├ 👥・**Всего:** `{users+bots}`
 ├ 👥・**Людей:** `{users}`
 └ 🤖・**Ботов:** `{bots}`
 🏆 〢**Инфо о владельце:**
 └ 👑・**Владелец сервера:** {owner}
""")
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
			await ctx.message.edit(content=f"""
 📑 〢**Информация о пользователе:**
 ├ 👥・**Ник юзера:** `{user.name}`
 ├ 🆔・**ID юзера:** `{user.id}`
 ├ 📸️・**Аватар юзера:** {user.avatar_url}
 ├ 🤖・**Бот:** `{bot}`
 ├ ⚒・**Создатель:** `{owner}`
 ├ 🔨・**Админ:** `{admin}`
 ├ 📈・**Самая высокая роль:** `@{user.top_role.name}`
 ├ 👁‍・**{voice}Статус:** `{status}`
 ├ 🔗・**Ссылка на профиль:** `https://discord.com/users/{user.id}`
 ├ 🕒・**Зашёл на сервер:** <t:{joinedat}> (<t:{joinedat}:R>)
 └ 🕒・**Аккаунт создан:** <t:{createdat}> (<t:{createdat}:R>)
""")
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
			await ctx.message.edit(content=f"""
 📑 〢**Информация о пользователе:**
 ├ 👥・**Ник юзера:** `{user.name}`
 ├ 🆔・**ID юзера:** `{user.id}`
 ├ 📸️・**Аватар юзера:** {user.avatar_url}
 ├ 🤖・**Бот:** `{bot}`
 ├ ⚒・**Создатель:** `{owner}`
 ├ 🔨・**Админ:** `{admin}`
 ├ 📈・**Самая высокая роль:** `@{user.top_role.name}`
 ├ 👁‍・**{voice}Статус:** `{status}`
 ├ 🔗・**Ссылка на профиль:** `https://discord.com/users/{user.id}`
 ├ 🕒・**Зашёл на сервер:** <t:{joinedat}> (<t:{joinedat}:R>)
 └ 🕒・**Аккаунт создан:** <t:{createdat}> (<t:{createdat}:R>)
""")
	@commands.command(aliases=['токен'])
	async def token(self, ctx, token):
		headers={'authorization': token}
		token_check = requests.get('https://discord.com/api/v9/users/@me/library',headers=headers)
		if token_check.status_code == 200 or token_check.status_code == 202:
			response=requests.get('https://discord.com/api/users/@me',headers=headers)
			r1=requests.get('https://discord.com/api/users/@me/channels',headers=headers)
			r2=requests.get("https://discord.com/api/v9/users/@me/relationships",headers=headers)
			r3=requests.get("https://discord.com/api/users/@me/guilds?with_counts=true",headers=headers)
			info=response.json()
			friends=len(r2.json())
			dms=len(r1.json())
			guilds=len(r3.json())
			await ctx.message.edit(content=f"""
 🔑 〢**Информация о токене:**
 ├ 👥・**Никнейм аккаунта:** `{info['username']}#{info['discriminator']}`
 ├ 🆔・**ID аккаунта:** `{info['id']}`
 ├ ✉️・**Email**: `{info['email']}`
 ├ 📱・**Номер телефона:** `{info['phone']}`
 ├ 🌎・**Страна:** `{info['locale']}`
 ├ 💬・**Открытых ЛС:** `{dms}`
 ├ 👥・**Друзей:** `{friends}`
 └ 🌎・**Серверов:** `{guilds}`
""")
		elif token_check.status_code == 401:
			await ctx.message.edit(content=f"**Токен** `{token}`**\nНе рабочий! :x:**")
		elif token_check.status_code == 403:
			response=requests.get('https://discord.com/api/users/@me',headers=headers)
			info=response.json()
			await ctx.message.edit(content=f"""
 🔑 〢**Информация о токене (требует подтверждения почты/телефона):**
 ├ 👥・**Никнейм аккаунта:** `{info['username']}#{info['discriminator']}`
 ├ 🆔・**ID аккаунта:** `{info['id']}`
 ├ ✉️・**Email**: `{info['email']}`
 ├ 📱・**Номер телефона:** `{info['phone']}`
 ├ 🌎・**Страна:** `{info['locale']}`
 ├ 💬・**Открытых ЛС:** `{dms}`
 ├ 👥・**Друзей:** `{friends}`
 └ 🌎・**Серверов:** `{guilds}`
""")
def setup(bot):
	bot.add_cog(Info(bot))
