import discord
from discord.ext import commands
import random, string
from asyncio import sleep

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def ascii(self, ctx, amount: int=1):
		await ctx.message.delete()
		for i in range(amount):
			text=''
			for i in range(2000):
				text=text+chr(random.randrange(13000))
			await ctx.send(content=text)
	@commands.command()
	async def hack(self, ctx, user:discord.User):
		perc=0
		while(perc < 100):
			await ctx.message.edit(content=f'**Получение почты `{user}`... {perc}%**')
			perc+=random.randint(1, 15)
		await ctx.message.edit(content='**:white_check_mark: Почта получена!**')
		await sleep(5)
		perc=0
		while(perc < 100):
			await ctx.message.edit(content=f'**Получение пароля `{user}`... {perc}%**')
			perc+=random.randint(1, 10)
		await ctx.message.edit(content='**:white_check_mark: Пароль был получен!**')
		await sleep(5)
		perc=0
		while(perc < 100):
			await ctx.message.edit(content=f'**Обход защиты... {perc}%**')
			perc+=random.randint(1, 5)
		await ctx.message.edit(content=f'**:white_check_mark: Успешно вошёл в аккаунт `{user}`**')
	@commands.command()
	async def rainbow(self, ctx):
		emojis=['🟧', '🟦', '🟥', '🟪', '🟩', '🟨']
		while True:
			text=''
			for i in range(300):
				text=text+''.join(random.choice(emojis))
			await ctx.message.edit(content=text)
		await ctx.message.delete()
	@commands.command()
	async def ghoul(self, ctx):
		await ctx.message.edit(content='```Я гуль...```')
		a=1000
		while a>6:
			await ctx.send(f'**{a}-7={a-7}**')
			a-=7
	@commands.command()
	async def boom(self, ctx):
		await ctx.message.edit(content="**Данный чат будет взорван через 5 секунд...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 4 секунды...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 3 секунды...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 2 секунды...**")
		await sleep(1)
		await ctx.message.edit(content="**Данный чат будет взорван через 1 секунду...**")
		await sleep(1)
		await ctx.message.delete()
		message=await ctx.send("**Boom!**", file=discord.File("Resources/boom.gif"))
		await sleep(1)
		await ctx.send("⠀" + "\n"*1998 + "⠀")
		await message.delete()
def setup(bot):
	bot.add_cog(Fun(bot))