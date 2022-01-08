import discord
from discord.ext import commands
import json
import requests

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def getchannels(self, ctx):
		channels=[]
		channels.append("**")
		channels.append("```Текстовые Каналы```\n")
		for channel in ctx.guild.text_channels:
			channels.append(f"{channel.mention} - `{channel.name}` `({channel.id})`\n")
		channels.append("\n```Голосовые Каналы```\n")
		for channel in ctx.guild.voice_channels:
			channels.append(f"{channel.mention} - `{channel.name}` `({channel.id})`\n")
		channels.append("\n```Категории```\n")
		for channel in ctx.guild.categories:
			channels.append(f"`{channel.name}` `({channel.id})`\n")
		channels.append("**")
		embed=discord.Embed(title=f"Все каналы {ctx.guild.name}", description=''.join(channels), color=0x8B0000)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text="Self bot By LALOL")
		try: await ctx.message.edit(content='', embed=embed)
		except:
			with open(f'Temp/channels_{ctx.guild.id}.txt', 'w', encoding='utf-8') as file:
				file.write(''.join(channels))
			await ctx.message.delete()
			await ctx.send(file=discord.File(f"Temp/channels_{ctx.guild.id}.txt"))
	@commands.command()
	async def channel(self, ctx, id: int):
		channel=self.bot.get_channel(id)
		try: testchannel=channel.category_id
		except:
			await ctx.message.edit(content="**:warning: Данного канала не существует или у вас нету доступа к нему!**", delete_after=3)
			return
		try: embed=discord.Embed(title=f"{channel.name}", description=f"**Имя: `{channel.name}`\nid: `{channel.id}`\nОписание: `{channel.topic}`\nТип: `TextChannel`\nСервер: `{channel.guild.name}`\nNsfw: `{channel.nsfw}`\nКатегория: `{channel.category_id}`\nПозиция: `{channel.position}`\nСлоумод: `{channel.slowmode_delay}s`\nСоздан: <t:{round(channel.created_at.timestamp())}:D>**", color=0x8B0000)
		except: embed=discord.Embed(title=f"{channel.name}", description=f"**Имя: `{channel.name}`\nid: `{channel.id}`\nТип: `VoiceChannel`\nБитрейт: 	`{channel.bitrate}`\nЛимит пользователей: `{channel.user_limit}`\nСервер: `{channel.guild.name}`\nКатегория: `{channel.category_id}`\nПозиция: `{channel.position}`\nСоздан: <t:{round(channel.created_at.timestamp())}:D>**", color=0x8B0000)
		embed.set_thumbnail(url=channel.guild.icon_url)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	@commands.command()
	async def role(self, ctx, id: int):
		for guild in self.bot.guilds:
			role=discord.utils.get(guild.roles, id=id)
			if not role is None:
				position=len(guild.roles)
				position=position-role.position
				embed=discord.Embed(title=f"{role.name}", description=f"**Имя: `{role.name}`\nid: `{role.id}`\nЦвет: `{role.colour}`\nПрава: `{role.permissions.value}`\nПингуется: `{role.mentionable}`\nСервер: `{role.guild.name}`\nПозиция: `{position}`\nСоздана: <t:{round(role.created_at.timestamp())}:D>**", color=0x8B0000)
				embed.set_thumbnail(url=role.guild.icon_url)
				embed.set_footer(text="Self bot By LALOL")
				await ctx.message.edit(content='', embed=embed)
				return
		await ctx.message.edit(content="**:warning: Данной роли не существует или у вас нет доступа к ней!**", delete_after=3)
	@commands.command()
	async def getroles(self, ctx):
		roles=[]
		roles1=ctx.guild.roles
		roles1.reverse()
		roles.append("**")
		for role in roles1:
			roles.append(f"{role.mention} - `{role.name}` `({role.id})`\n")
		roles.append("**")
		embed=discord.Embed(title=f"Все роли {ctx.guild.name}", description=''.join(roles), color=0x8B0000)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text="Self bot By LALOL")
		try: await ctx.message.edit(content='', embed=embed)
		except:
			with open(f'Temp/roles_{ctx.guild.id}.txt', 'w', encoding='utf-8') as file:
				file.write(''.join(roles))
			await ctx.message.delete()
			await ctx.send(file=discord.File(f"Temp/roles_{ctx.guild.id}.txt"))
	@commands.command()
	async def getemojis(self, ctx):
		emojis=[]
		emojis.append("**")
		emojis.append("```Эмодзи```\n")
		for emoji in ctx.guild.emojis:
			if not emoji.animated:
				emojis.append(f"<:{emoji.name}:{emoji.id}> - `{emoji.name}` `({emoji.id})`\n")
		emojis.append("```Анимированные Эмодзи```\n")
		for emoji in ctx.guild.emojis:
			if emoji.animated:
				emojis.append(f"<:{emoji.name}:{emoji.id}> - `{emoji.name}` `({emoji.id})`\n")
		emojis.append("**")
		embed=discord.Embed(title=f"Все эмодзи {ctx.guild.name}", description=''.join(emojis), color=0x8B0000)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text="Self bot By LALOL")
		try: await ctx.message.edit(content='', embed=embed)
		except:
			with open(f'Temp/emojis_{ctx.guild.id}.txt', 'w', encoding='utf-8') as file:
				file.write(''.join(emojis))
			await ctx.message.delete()
			await ctx.send(file=discord.File(f"Temp/emojis_{ctx.guild.id}.txt"))
	@commands.command()
	async def emoji(self, ctx, id: int):
		emoji=self.bot.get_emoji(id)
		try: embed=discord.Embed(title=emoji.name, description=f"**Имя: `{emoji.name}`\nid: `{emoji.id}`\nАнимирован: `{emoji.animated}`\nСервер: `{emoji.guild.name}`\nСоздано: <t:{round(emoji.created_at.timestamp())}:D>**", color=0x8B0000)
		except:
			await ctx.message.edit(content="**:warning: Данного эмодзи не существует или у вас нет доступа к нему!**", delete_after=3)
			return
		embed.set_thumbnail(url=emoji.url)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	@commands.command()
	async def getmessages(self, ctx, amount: int):
		await ctx.message.delete()
		messages1 = await ctx.channel.history(limit=amount).flatten()
		messages1.reverse()
		messages=[]
		for message in messages1:
			messages.append(f"{message.author}: {message.content}\n")
		with open(f'Temp/messages_{ctx.channel.id}.txt', 'w', encoding='utf-8') as file:
			file.write(''.join(messages))
		await ctx.send(file=discord.File(f"Temp/messages_{ctx.channel.id}.txt"))
	@commands.command()
	async def guild(self, ctx):
		createdat=round(ctx.guild.created_at.timestamp())
		embed=discord.Embed(title="Информация о Сервере", description=f"**Название: `{ctx.guild.name}`\nid: `{ctx.guild.id}`\nУчастников: `{ctx.guild.member_count}`\nВладелец: `{ctx.guild.owner}`\nТекстовых каналов: `{len(ctx.guild.text_channels)}`\nГолосовых каналов: `{len(ctx.guild.voice_channels)}`\nКатегорий: `{len(ctx.guild.categories)}`\nРолей: `{len(ctx.guild.roles)}`\nСоздан: <t:{createdat}:D>**", color=0x8B0000)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	@commands.command()
	async def user(self, ctx, *, user:discord.User):
		createdat=round(user.created_at.timestamp())
		embed=discord.Embed(title=user, description=f"**Имя: `{user.name}`\nТег: `{user.discriminator}`\nid: `{user.id}`\nБот: `{user.bot}`\nДата регистрации Аккаунта: <t:{createdat}:D>**", color=0x8B0000)
		embed.set_thumbnail(url=user.avatar_url)
		req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
		banner_id = req["banner"]
		if banner_id:
			embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024")
		embed.set_footer(text="Self bot By LALOL")
		await ctx.message.edit(content='', embed=embed)
	@commands.command()
	async def invite(self, ctx, *, link):
		if "discord.gg/" in link:
			link2 = (link.split("https://discord.gg/")[1])[:10]
			response = requests.get(f'https://discord.com/api/v6/invite/{link2}').json()
			if 'Unknown Invite' in response:
				await ctx.message.edit(content="**:warning: Неправильная ссылка приглашения!**", delete_after=3)
			else:
				try: embed=discord.Embed(title=link, description=f"**Имя Сервера: `{response['guild']['name']}`\nid Сервера: `{response['guild']['id']}`\nИмя Создателя приглашения: `{response['inviter']['username']}`\nТег Создателя приглашения: `{response['inviter']['discriminator']}`\nid Создателя приглашения: `{response['inviter']['id']}`\nИмя Канала: `{response['channel']['name']}`\nid Канала: `{response['channel']['id']}`**", color=0x8B0000)
				except:
					await ctx.message.edit(content="**:warning: Неправильная ссылка приглашения!**", delete_after=3)
					return
				embed.set_thumbnail(url=f"https://cdn.discordapp.com/icons/{response['guild']['id']}/{response['guild']['icon']}")
				embed.set_footer(text="Self bot By LALOL")
				await ctx.message.edit(content='', embed=embed)
		else:
			await ctx.message.edit(content="**:warning: Укажите пожалуйста ссылку приглашения в формате\n<https://discord.gg/код_ссылки_приглашения>**", delete_after=5)
def setup(bot):
	bot.add_cog(Info(bot))