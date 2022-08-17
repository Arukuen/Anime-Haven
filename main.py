import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import discord_interface

# Module for fetching hentai is currently not working

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='+')


@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}')


@bot.command(name='anime')
async def anime(ctx, *args):
	rank = int(args[0])
	search_term = ' '.join(args[1:])
	author = ctx.message.author

	anime = discord_interface.add_anime(author.name, author.id, search_term, rank)
	if isinstance(anime, str):
		await ctx.send(anime)
	else:
		await ctx.send(f'**{anime.title}** added by ***{author.name}*** with rank ***{anime.rank}***')
		image = discord.Embed()
		image.set_image(url=anime.image_url)
		await ctx.send(embed=image)


@bot.command(name='char')
async def character(ctx, *args):
	rank = int(args[0])
	search_term = ' '.join(args[1:])
	author = ctx.message.author

	character = discord_interface.add_character(author.name, author.id, search_term, rank)
	if isinstance(character, str):
		await ctx.send(character)
	else:
		await ctx.send(f'**{character.name}** added by ***{author.name}*** with rank ***{character.rank}***')
		image = discord.Embed()
		image.set_image(url=character.image_url)
		await ctx.send(embed=image)


@bot.command(name='anime_list')
async def anime_list(ctx, *args):
	username = ' '.join(args)
	anime_list = discord_interface.list_anime(username)
	if not type(anime_list) == list:
		await ctx.send(anime_list)
	else:
		response = ''
		for anime in anime_list:
			response = f'{response}\n{anime.rank}. {anime.title}'
		await ctx.send(response)


@bot.command(name='char_list')
async def char_list(ctx, *args):
	username = ' '.join(args)
	char_list = discord_interface.list_character(username)
	if not type(char_list) == list:
		await ctx.send(char_list)
	else:
		response = ''
		for char in char_list:
			response = f'{response}\n{char.rank}. {char.name}'
		await ctx.send(response)


bot.run(TOKEN)


