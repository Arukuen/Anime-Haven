import discord
import anime_fetcher
import os
from dotenv import load_dotenv

# Module for fetching hentai is currently not working

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

database = {
	'user': {}
}

def add_anime_to_user(username, anime_title, rank):
	if username not in database['user'].keys():
		database['user'][username] = [anime_title]
	else:
		#print(rank, len(database['user']))
		if rank > len(database['user'][username]):
			database['user'][username].append(anime_title)
		else:
			database['user'][username].insert(rank-1, anime_title)

def list_user(username):
	if username in database['user'].keys():
		numbered_list = [f'{index+1}. {anime}' for index, anime in enumerate(database['user'][username])]
		return "\n".join(numbered_list)
	return "Username Invalid"

def insert_anime_to_user(username, anime, rank):
	pass
 

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

@client.event
async def on_message(message):

	msg = message.content
	author = message.author

	if msg.startswith("+anime "):
		splitted = msg.split()
		rank = int(splitted[1])
		title = ' '.join(splitted[2:])
	
		clean_title, image_url = anime_fetcher.search_anime(title)

		add_anime_to_user(author.name, clean_title, rank)		

		#print(f'{clean_title} added by {author.name} with rank {rank}')
		await message.channel.send(f'**{clean_title}** added by ***{author.name}*** with rank ***{rank}***')

		image = discord.Embed()
		image.set_image(url=image_url)
		await message.channel.send(embed=image)
		

	if msg.startswith("+userlist "):
		username = msg.split("+userlist ")[1]
		await message.channel.send(list_user(username))



client.run(TOKEN)


