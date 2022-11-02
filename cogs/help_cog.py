#!/usr/bin/env python3

from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        message = ("```List of commands:\n"
                   "\n"
                   ",p - Play a song via Youtube/Soundcloud link or search by keywords. If a song is already playing, put the new one in queue.\n"
                   ",s - Skip the current song.\n"
                   ",loop - Loop the current song.\n"
                   ",queue - Show the current queue.\n"
                   ",remove - Remove the specified song from the queue (use order number from ,queue).\n"
                   ",pause - Pause playback.\n"
                   ",resume - Resume playback.\n"
                   ",skipall - Empty queue and skip the current song.\n"
                   ",leave - Ask the bot to leave the current channel.\n"
                   ",delete - Delete the specified amount of bot's messages from the channel (default 10).\n"
                   ",help - List the available commands.```")
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Help(bot))
