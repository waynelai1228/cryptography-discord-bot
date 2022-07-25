from cryptography.fernet import Fernet
import discord
import os

key = Fernet.generate_key()

fnet = Fernet(key)

TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global key
    global fnet
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('--------------')
        await message.channel.send('Hello!')

    if message.content.startswith('$decrypt'):
        ptext = message.content.split('$decrypt', 1)[1]
        await message.delete()
        try:
          dectext = fnet.decrypt(ptext.encode('utf-8'))
          print(ptext, dectext)
          await message.channel.send('--------------')
          await message.channel.send(dectext.decode('utf-8'), delete_after=10.0)
        except:
          await message.channel.send('--------------')
          await message.channel.send('invalid key')

    if message.content.startswith('$encrypt'):
        ptext = message.content.split('$encrypt', 1)[1]
        enctext = fnet.encrypt(ptext.encode('utf-8'))
        print(ptext, enctext)
        await message.delete()
        await message.channel.send('--------------')
        await message.channel.send('{0}: {1}'.format(message.author, enctext.decode('utf-8')))

    if message.content.startswith('$key'):
        await message.delete()
        await message.channel.send('--------------')
        await message.channel.send(key.decode('utf-8'), delete_after=10.0)

    if message.content.startswith('$generatekey'):
        await message.delete()
        key = Fernet.generate_key()
        fnet = Fernet(key)

    if message.content.startswith('$setkey'):
        ptext = message.content.split('$setkey', 1)[1]
        key = ptext.encode('utf-8')
        fnet = Fernet(key)
        await message.delete()

client.run(TOKEN)
