import discord
from discord.ext import commands
import random, string
from asyncio import sleep

troll={'server_id': 0, 'user_id': 0}

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def troll(self, ctx, user:discord.Member):
		await ctx.message.delete()
		global troll
		troll['server_id']=ctx.guild.id
		troll['user_id']=user.id
	@commands.command()
	async def untroll(self, ctx):
		await ctx.message.delete()
		global troll
		troll['user_id']=0
	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			if message.author.id==troll['user_id'] and message.guild.id==troll['server_id']:
				await message.delete()
		except:return
	@commands.command(aliases=['react', 'reactions', 'реакция', 'реакции', 'reactionall'])
	async def reaction(self, ctx, emoji, amount: int=15):
		await ctx.message.delete()
		messages=await ctx.channel.history(limit=amount).flatten()
		reactioned=0
		for message in messages:
			await message.add_reaction(emoji)
			reactioned+=1
		await ctx.send(f"**__Selfbot by LALOL__\n\n:white_check_mark: Успешно поставил {reactioned} реакций!**")
def setup(bot):
	bot.add_cog(Fun(bot))
