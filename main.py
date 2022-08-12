import discord
import anime_fetcher
import os
import discord_interface
from dotenv import load_dotenv

# Module for fetching hentai is currently not working

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

database = {
	'user': {}
}


# Obsolete functions
# def add_anime_to_user(username, anime_title, rank):
# 	if username not in database['user'].keys():
# 		database['user'][username] = [anime_title]
# 	else:
# 		#print(rank, len(database['user']))
# 		if rank > len(database['user'][username]):
# 			database['user'][username].append(anime_title)
# 		else:
# 			database['user'][username].insert(rank-1, anime_title)

# def list_user(username):
# 	if username in database['user'].keys():
# 		numbered_list = [f'{index+1}. {anime}' for index, anime in enumerate(database['user'][username])]
# 		return "\n".join(numbered_list)
# 	return "Username Invalid"




@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
	msg = message.content
	author = message.author

	if msg.startswith('+anime ') or msg.startswith('+add '):
		splitted = msg.split()
		rank = int(splitted[1])
		search_term = ' '.join(splitted[2:])
		anime = discord_interface.add(author.name, author.id, search_term, rank)
		if not isinstance(anime, anime_fetcher.Anime):
			await message.channel.send(anime)
		else:
			await message.channel.send(f'**{anime.title}** added by ***{author.name}*** with rank ***{rank}***')
			image = discord.Embed()
			image.set_image(url=anime.image_url)
			await message.channel.send(embed=image)


	if msg.startswith('+userlist ') or msg.startswith('+user '):
		username = msg.split()[1]
		anime_list = discord_interface.userlist(username)
		if not type(anime_list) == list:
			await message.channel.send(anime_list)
		else:
			for anime in anime_list:
				await message.channel.send(anime.title)


	if msg == '+help' or msg == '+anime haven':
		await message.channel.send('''
Anime Haven is a bot for ranking your favorite anime for others to see. Below are the available commands:

**+anime [rank] [title]**
Adds the anime with the specified title to the user’s list following the provided rank. If another anime already exist with the same rank on the list, the new anime replaces it, and the old anime moves down the rank.
Examples:
+anime 1 boku no pico 
+anime 2 sao 
+anime 3 lycoris recoil 
+anime 4 domestic girlfriend 

**+userlist [username]**
View the list of anime of the user with the provided username.
Example:
+userlist Arukuen
		''')


client.run(TOKEN)


