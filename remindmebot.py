# bot.py
import time
import asyncio
from threading import Thread, Lock
import os
import discord
from discord.ext import commands
import dotenv

class RemindMeThread(Thread):
    reminders = {}
    lock = Lock()
    def run(self):
        while 1:
            time.sleep(30)
            self.lock.acquire()
            try:
                if self.reminders == {}:
                    print("No reminders to track")
                else:
                    ct = time.time()
                    print("Reminders on hold:")
                    for i in self.reminders.copy():
                        print(self.reminders[i][2])
                        '''if self.reminders[i][0] <= ct:
                            msg = self.reminders[i][2]
                            ctx = self.reminders[i][1]
                            ctx.author.send(msg)
                            self.reminders.pop(i)'''
            finally:
                self.lock.release()

    def addreminder(self, t, u, msg):
        '''
        Add a new reminder to send message msg to user u at time t
        '''
        k = str(t) + str(u)
        self.reminders[k] = [t, u, msg]
        return

    def purge(self):
        self.lock.acquire()
        try:
            for i in self.reminders.copy():
                self.reminders.pop(i)
        finally:
            self.lock.release()



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
    print(ctx.author)
    await ctx.send("Hello!")

    if ctx.message.tts:
        await ctx.send('I heard that!')

@bot.command(name='remindme')
async def remindme(ctx):
    if ctx.author == bot.user:
        return
    t = time.time()
    t = t + 60.00
    await ctx.send("I will remind you in 60 seconds")
    reminders.addreminder(t, ctx, ctx.message.content)
    await asyncio.sleep(60)
    await ctx.author.send(ctx.message.content.strip('$remindme'))


@bot.command(name="purge")
async def purge(ctx):
    if ctx.author == bot.user:
         return
    reminders.purge()
    await ctx.send("Purge command confirmed. Now deleting all reminders.")

bot.run(TOKEN)
