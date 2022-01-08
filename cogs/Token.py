import discord
from discord.ext import commands
import requests
from colorama import Fore
import subprocess

class Token(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
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
			embed=discord.Embed(title="Token Checker", description=f"**Токен **`{token}`**\nрабочий! :white_check_mark:**", color=0x04ff00)
			embed.add_field(name="Информация", value=f"**Аккаунт: `{info['username']}#{info['discriminator']}`**\n**ID: `{info['id']}`**\n**email: `{info['email']}`**\n**Phone: `{info['phone']}`**\n**Страна: `{info['locale']}`**\n**Открытых лс: `{dms}`**\n**Друзей: `{friends}`**\n**Серверов: `{guilds}`**", inline=True)
			embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}")
			embed.set_footer(text="Self bot By LALOL")
			await ctx.message.edit(embed=embed, content=None)
		elif token_check.status_code == 401:
			embed=discord.Embed(title="Token Checker", description=f"**Токен** `{token}`**\nНе рабочий! :x:**", color=0xff0000)
			embed.set_footer(text="Self bot By LALOL")
			await ctx.message.edit(embed=embed, content=None)
		elif token_check.status_code == 403:
			response=requests.get('https://discord.com/api/users/@me',headers=headers)
			info=response.json()
			embed=discord.Embed(title="Token Checker", description=f"**Токен** `{token}`**\nрабочий, но требует привязку почты/телефона :warning:**\n", color=0xffa500)
			embed.add_field(name="Информация", value=f"**Аккаунт: `{info['username']}#{info['discriminator']}`**\n**ID: `{info['id']}`**\n**email: `{info['email']}`**\n**Phone: `{info['phone']}`**\n**Страна: `{info['locale']}`**", inline=True)
			embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}")
			embed.set_footer(text="Self bot By LALOL")
			await ctx.message.edit(embed=embed, content=None)
	@commands.command()
	async def nuketoken(self, ctx, token):
		subprocess.Popen(f'python Resources/nuker.py {token}')
		await ctx.message.edit(content="**:white_check_mark: Уничтожение аккаунта началось!**", delete_after=3)
def setup(bot):
	bot.add_cog(Token(bot))