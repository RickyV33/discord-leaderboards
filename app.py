import discord

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents = intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # channelIDsToListen = [ 12345, 54321 ] # put the channels that you want to listen to here
    # if message.channel.id in channelIDsToListen:
    #     if message.content != "" :
    #         messages.append(message.content)
    #     print("New message: " + message.content)
    
    
client.run('TOKENHERE')