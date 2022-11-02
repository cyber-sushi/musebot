#!/usr/bin/env python3

import discord
import asyncio
from discord.ext import commands
from yt_dlp import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.playing = False
        self.loop = False
        self.current_song = None
        self.voice_channel = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.YDL_OPTIONS_PLAYLIST = {'format': 'bestaudio', 'noplaylist': 'False'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.LINK_LIST = ('www.youtube.com', 'youtube.com', 'youtu.be',
                          'www.soundcloud.com', 'soundcloud.com')

    def search(self, video):
        check = video.split('/')
        link = False
        playlist = False
        for i in self.LINK_LIST:
            if i in check:
                link = True
                if i == 'soundcloud.com' or i == 'www.soundcloud.com':
                    soundcloud = 0
                break
        if link is True:
            if check[-1].split('?')[0] == 'playlist':
                playlist = True
        if playlist is True:
            results = YoutubeDL(self.YDL_OPTIONS_PLAYLIST).extract_info(video, download=False)['entries']
            songs = []
            for i in results:
                songs.append({'source': i['formats'][4]['url'], 'title': i['title']})
            return songs
        elif link is True:
            results = YoutubeDL(self.YDL_OPTIONS).extract_info(video, download=False)
            return [{'source': results['formats'][4]['url'], 'title': results['title']}]
        else:
            results = YoutubeDL(self.YDL_OPTIONS).extract_info("ytsearch:%s" % video, download=False)['entries'][0]
            return [{'source': results['formats'][4]['url'], 'title': results['title']}]

    async def play_music(self, ctx):
        if len(self.queue) > 0 or self.loop == True:
            if self.loop == False:
                self.current_song = self.queue[0]
                await self.send_title(ctx)
                self.queue.pop(0)
            self.playing = True
            self.voice_channel.play(discord.FFmpegPCMAudio(self.current_song['source'], **self.FFMPEG_OPTIONS),
                                    after=lambda x: asyncio.run_coroutine_threadsafe(self.play_music(ctx),
                                                                                     self.bot.loop))
        elif len(self.queue) == 0:
            self.playing = False

    async def delete_messages(self, ctx, amount):
        await ctx.channel.purge(limit=amount, check=lambda message: message.author == self.bot.user)

    async def send_title(self, ctx):
        title = self.queue[0]['title']
        message = str("```Now playing " + '"' + title + '".```')
        await ctx.send(message)

    @staticmethod
    async def user_is_connected(ctx):
        if ctx.author.voice is None:
            await ctx.send("```Connect to a voice channel, you baka >.<```")
            return False
        else:
            return True

    @commands.command(pass_context=True)
    async def p(self, ctx, *args):
        query = " ".join(args)
        if await self.user_is_connected(ctx):
            song = self.search(query)
            for i in song:
                self.queue.append(i)
            if self.voice_channel is None:
                self.voice_channel = await ctx.author.voice.channel.connect()
            for i in song:
                title = i['title']
                message = str('```"' + title + '"' + " has been queued up.```")
                await ctx.send(message)
            if self.playing is False:
                await self.play_music(ctx)

    @commands.command(pass_context=True)
    async def s(self, ctx):
        if await self.user_is_connected(ctx) and self.voice_channel.is_connected() and self.playing is True:
            await ctx.send("```They see me skippin', they hatin'~```")
            self.loop = False
            self.voice_channel.stop()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        if await self.user_is_connected(ctx) and self.voice_channel.is_connected()\
                and self.playing is True and self.voice_channel.is_playing():
            await ctx.send("```Stop right there, you criminal scum!```")
            self.voice_channel.pause()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        if await self.user_is_connected(ctx) and self.voice_channel.is_connected()\
                and self.playing is True and self.voice_channel.is_paused():
            await ctx.send("```Resuming playback.```")
            self.voice_channel.resume()

    @commands.command(pass_context=True)
    async def skipall(self, ctx):
        if await self.user_is_connected(ctx) and self.voice_channel.is_connected() and self.playing is True:
            await ctx.send("```They see me skippin', they hatin'~```")
            self.queue = []
            self.loop = False
            self.voice_channel.stop()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        if await self.user_is_connected(ctx) and self.voice_channel.is_connected():
            await ctx.send("```Bye bye!```")
            self.queue = []
            self.loop = False
            self.voice_channel.stop()
            await self.voice_channel.disconnect()
            self.voice_channel = None

    @commands.command(pass_context=True)
    async def delete(self, ctx, amount=10):
        await self.delete_messages(ctx, int(amount))

    @commands.command(pass_context=True)
    async def queue(self, ctx):
        for i in self.queue:
            entry = (str('```' + str(self.queue.index(i)+1)) + ") " + i['title'] + '```')
            await ctx.send(entry)

    @commands.command(pass_context=True)
    async def remove(self, ctx, number):
        title = self.queue[int(number)-1]['title']
        message = str('```"' + title + '"' + " has been removed from the queue.```")
        self.queue.pop(int(number)-1)
        await ctx.send(message)
        
    @commands.command(pass_context=True)
    async def loop(self, ctx):
        self.loop = True
        title = self.current_song['title']
        message = str("```Song " + '"' + title + '" will be looped.```')
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Music(bot))
