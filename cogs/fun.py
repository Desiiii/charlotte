# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import weeb
import os.path
import ujson
import random
import urllib.parse

class Fun:
    """W-want to have some f-fun with me?"""

    def __init__(self, bot):
        self.bot = bot
        self.weeb = weeb.Client(token=bot.config.weebsh, user_agent="Weeb.py/1.1.0")

    @commands.command()
    async def explosion(self, ctx):
        url = await self.bot.session.get('https://megumin.torque.ink/api/explosion')
        res = await url.json()

        if res is None:
            return await ctx.send('Something broke. Try again later?')

        e = discord.Embed(color=discord.Color.red(), title='Explosion!')
        e.description = res['chant']
        e.set_image(url=res['img'])
        e.set_footer(text='Powered by megumin.torque.ink')
        await ctx.send(embed=e)

    @commands.command()
    async def urban(self, ctx, *, term: str):
        """Find the definition to \"wagwan\" or something """

        term = urllib.parse.quote_plus(term) # make the search term url-safe

        url = await self.bot.session.get(f'http://api.urbandictionary.com/v0/define?term={term}')
        res = await url.json()

        if res is None:
            return await ctx.send("I think the API broke... Erm, wut?")

        count = len(res['list'])
        if count == 0:
            return await ctx.send("Couldn't find your search in the dictionary...")
        result = res['list'][random.randint(0, count - 1)]

        definition = result['definition']
        if len(definition) >= 1000:
            definition = definition[:1000]
            definition = definition.rsplit(' ', 1)[0]
            definition += '...'

        embed = discord.Embed(colour=0xcf5c36, description=f"**{result['word']}**\n*by: {result['author']}*")
        embed.add_field(name='Definition', value=definition, inline=False)
        embed.add_field(name='Example', value=result['example'], inline=False)
        embed.set_footer(text=f"👍 {result['thumbs_up']} | 👎 {result['thumbs_down']}")
        embed.set_author(name=f"Requested by {ctx.author.name}",
                         url=f"http://api.urbandictionary.com/v0/define?term={term}",
                         icon_url=ctx.author.avatar_url)

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I found something, but have no access to post it... [Embed permissions]")
    
    @commands.command()
    async def cat(self, ctx):
        '''Get a random cat image.'''
        
        fact = await self.bot.session.get(url='https://catfact.ninja/fact')
        fact = await fact.json()
        e = discord.Embed(color=ctx.author.color, description=fact['fact'])
        resp = await self.bot.session.get(url='https://aws.random.cat/meow')
        resp = ujson.loads(await resp.text())
        e.set_image(url=resp['file'])

        e.set_footer(text='Powered by random.cat')
        await ctx.send(embed=e)

    @commands.command()
    async def dog(self, ctx):
        '''Get a random dog image.'''
        e = discord.Embed(color=ctx.author.color)
        resp = await self.bot.session.get(url='https://random.dog/woof.json')
        resp = await resp.json()
        e.set_image(url=resp['url'])
        e.set_footer(text='Powered by random.dog')
        await ctx.send(embed=e)

    @commands.command()
    async def birb(self, ctx):
        '''Get a random birb image.'''
        e = discord.Embed(color=ctx.author.color)
        resp = await self.bot.session.get(url='https://random.birb.pw/tweet.json')
        resp = await resp.json(content_type='text/plain')
        e.set_image(url=f'https://random.birb.pw/img/{resp["file"]}')
        e.set_footer(text='Powered by random.birb.pw')
        await ctx.send(embed=e)

    @commands.command()
    async def neko(self, ctx):
        '''Gets a random neko :3'''
        e = discord.Embed(color=ctx.author.color)
        resp = await self.bot.session.get(url='https://nekos.life/api/neko')
        resp = await resp.json()
        e.set_image(url=resp['neko'])
        e.set_footer(text='Powered by nekos.life')
        await ctx.send(embed=e)

    @commands.command()
    @commands.is_nsfw()
    async def lewdneko(self, ctx):
        '''Gets a random lewd neko o.o'''
        e = discord.Embed(color=ctx.author.color)
        resp = await self.bot.session.get(url='https://nekos.life/api/lewd/neko')
        resp = await resp.json()
        e.set_image(url=resp['neko'])
        e.set_footer(text='Powered by nekos.life')
        await ctx.send(embed=e)

    @commands.command()
    async def xkcd(self, ctx, number=None):
        '''Get an xkcd comic.'''
        try:
            number = int(number)
        except:
            if number is not None:
                return await ctx.send('Can you do math baka?! That\'s not a number! >~<')
        if isinstance(number, int):
            ra = await self.bot.session.get(url=f'https://xkcd.com/{number}/info.0.json')
            r = await ra.json()
        else:
            raw = await self.bot.session.get(url='https://xkcd.com/info.0.json')
            r = await raw.json()
        
        e = discord.Embed(title=r['safe_title'], description='xkcd - {}\n\n{}'.format(r['num'], r['alt']))
        e.set_image(url=r['img'])
        e.set_footer(text=f'{r["month"]}/{r["day"]}/{r["year"]} (mm/dd/yyyy)', icon_url='https://i.imgur.com/9sSBA52.jpg')
        await ctx.send(embed=e)

    @commands.command()
    async def pat(self, ctx, user: discord.User=None):
        '''Pat someone.'''
        img = await self.weeb.get_image(imgtype='pat')
        if user:
            if user.id == ctx.author.id:
                e = discord.Embed(description=f'{ctx.author.name} was feeling lonely so I gave them a pat!')
            elif user.id == self.bot.user.id:
                e = discord.Embed(description=f'B-Baka!')
                e.set_image(url='https://data.whicdn.com/images/65768241/large.gif')
                return await ctx.send(embed=e)
            else:
                e = discord.Embed(description=f'{ctx.author.name} patted {user.name}')
        else:
            e = discord.Embed()
        e.set_image(url=img[0])
        e.set_footer(text='Powered by weeb.sh')
        await ctx.send(embed=e)

    @commands.command(aliases=['weeb', 'weebsh'])
    async def action(self, ctx, type=None):
        '''Fetch a type from weeb.sh. Call without args to get a list of types.'''
        types = await self.weeb.get_types()
        if type and type in types:
            e = discord.Embed()
            i = await self.weeb.get_image(imgtype=type)
            e.set_image(url=i[0])
            e.set_footer(text='Powered by weeb.sh')
            await ctx.send(embed=e)
        else:
            types = ', '.join(f'`{type}`' for type in types)
            await ctx.send(content=f'Invalid Type - Here\'s a list of valid types:\n\n{types}')

    @commands.command()
    async def slap(self, ctx, user: discord.User=None):
        '''Slap someone.'''
        img = await self.weeb.get_image(imgtype='slap')
        if user:
            if user.id == ctx.author.id:
                e = discord.Embed(description=f'{ctx.author.name} slapped themselves \o/')
            elif user.id == self.bot.user.id:
                e = discord.Embed(description=f'N-nooo! Baka!')
            else:
                e = discord.Embed(description=f'{ctx.author.name} slapped {user.name} \o/')
        else:
            e = discord.Embed()
        e.set_image(url=img[0])
        await ctx.send(embed=e)

    @commands.command()
    async def waifuinsult(self, ctx, user:discord.User=None):
        '''Insults somebody's waifu.'''
        if user is None:
            user = ctx.author
        async with ctx.typing(): 
            if not os.path.isfile(f'cache/waifuinsult/{user.id}.webp'):
                with open(f'cache/waifuinsult/{user.id}.webp', 'wb') as f:
                    f.write(await self.weeb.generate_waifu_insult(avatar=user.avatar_url))

            with open(f'cache/waifuinsult/{user.id}.webp', 'rb') as f:
                await ctx.send(file=discord.File(fp=f))

    @commands.command()
    async def ship(self, ctx, user:discord.User, user2:discord.User):
        '''Ships two users.'''
        async with ctx.typing(): 
            if not os.path.isfile(f'cache/ship/{user.id}-{user2.id}.webp'):
                with open(f'cache/ship/{user.id}-{user2.id}.webp', 'wb') as f:
                    f.write(await self.weeb.generate_love_ship(target_one=user.avatar_url, target_two=user2.avatar_url))

            with open(f'cache/ship/{user.id}-{user2.id}.webp', 'rb') as f:
                await ctx.send(file=discord.File(fp=f))

    @commands.command(aliases=['roll', 'dice'])
    async def rtd(self, ctx):
        '''Rolls a die.'''
        await ctx.send(f'I-I have to choose? I\'m not sure... I pick... **{random.randint(1, 6)}**')

    @commands.command(aliases=['choose'])
    async def pick(self, ctx, *, choices):
        '''Picks a random choice. Choices must be separated by ' | '.'''
        choice = random.choice(choices.split(' | ')) 
        await ctx.send(f'Mmm... I pick... **{choice}**')


def setup(bot):
    bot.add_cog(Fun(bot))
