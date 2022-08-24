import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import discord_interface

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Logged in as {self.user}.')

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)


@tree.command(name = 'anime', description = "Adds anime to user's list")
async def anime(interaction: discord.Interaction, rank: int, search_term: str):
	author = interaction.user

	anime = discord_interface.add_anime(author.name, author.id, search_term, rank)
	if isinstance(anime, str):
		await interaction.response.send_message(content = anime)
	else:
		image = discord.Embed()
		image.set_image(url=anime.image_url)
		await interaction.response.send_message(content = f'**{anime.title}** added by ***{author.name}*** with rank ***{anime.rank}***', embed = image)


@tree.command(name = 'char', description = "Adds character to user's list")
async def char(interaction: discord.Interaction, rank: int, search_term: str):
	author = interaction.user

	character = discord_interface.add_character(author.name, author.id, search_term, rank)
	if isinstance(character, str):
		await interaction.response.send_message(character)
	else:
		image = discord.Embed()
		image.set_image(url=character.image_url)
		await interaction.response.send_message(content = f'**{character.name}** added by ***{author.name}*** with rank ***{character.rank}***', embed = image)
		

@tree.command(name = 'anime_list', description = "Show user's list of anime")
async def anime_list(interaction: discord.Interaction, username: str):
	anime_list = discord_interface.list_anime(username)
	if not type(anime_list) == list:
		await interaction.response.send_message(anime_list)
	else:
		response = ''
		for anime in anime_list:
			response = f'{response}\n{anime.rank}. {anime.title}'
		await interaction.response.send_message(response)


@tree.command(name = 'char_list', description = "Show user's list of characters")
async def char_list(interaction: discord.Interaction, username: str):
	char_list = discord_interface.list_character(username)
	if not type(char_list) == list:
		await interaction.response.send_message(char_list)
	else:
		response = ''
		for char in char_list:
			response = f'{response}\n{char.rank}. {char.name}'
		await interaction.response.send_message(response)


client.run(TOKEN)


