#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio

with open('token.txt') as t:
    token = t.read()

async def start_bot():
    bot = commands.Bot(command_prefix=',', intents=discord.Intents.all(), help_command=None)
    await bot.load_extension('cogs.music_cog')
    await bot.load_extension('cogs.help_cog')
    return bot

if __name__ == '__main__':
    bot = asyncio.run(start_bot())
    bot.run(f'{token}')
