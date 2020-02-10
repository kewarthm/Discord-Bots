# bot.py
import time
from threading import Thread
import os
import discord
from discord.ext import commands
import dotenv

class RemindMeThread(Thread):
    reminders = {}
    def run(self):
        while 1:
            time.sleep(30)
            if self.reminders == {}:
                print("No reminders to track")

    def addreminder(self, t, u, msg):
        '''
        Add a new reminder to send message msg to user u at time t
        '''
        return

#Load token and valid guilds from env file
dotenv.load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='$')
reminders = RemindMeThread()
reminders.start()
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.command(name='hello')
async def greet(ctx):
    if ctx.author == bot.user:
        return
    await ctx.send("Hello!")

    if ctx.message.tts:
        await ctx.send('I heard that!')


bot.run(TOKEN)
