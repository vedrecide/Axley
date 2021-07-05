import discord
import textwrap
import io
import contextlib
import re
import zlib
import aiohttp
import os

from discord.ext import commands
from utils.paginator import clean_code
from utils.paginator import Pag
from traceback import format_exception



class SphinxObjectFileReader:
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode("utf-8")

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b""
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b"\n")
            while pos != -1:
                yield buf[:pos].decode("utf-8")
                buf = buf[pos + 1:]
                pos = buf.find(b"\n")


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis

    @commands.command(name='Eval', description='Evaluates a Python code', hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        code = clean_code(code)

        local_variables = {
            'discord': discord,
            'commands': commands,
            'self': self.bot,
            'ctx': ctx
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f'async def func():\n{textwrap.indent(code,"    ")}', local_variables,)

                obj = await local_variables['func']()
                result = f'{stdout.getvalue()}\n>>> {obj}\n'
        except Exception as e:
            result = ''.join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix='```py\n',
            suffix='```',
            colour=0xc67862,
            title='{} Output'.format(self.emojis['tick']),
        )

        await pager.start(ctx)

    @commands.command(name='Reload', description='Reloads a cog..', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.reload_extension(f'{cog}')
            embed = discord.Embed(
                color=discord.Color.dark_theme(),
                description='{} Successfully reloaded `{}`'.format(
                    self.emojis['tick'], cog)
            )
            await ctx.message.add_reaction('✅')
            await ctx.message.reply(embed=embed, mention_author=False)
        except Exception as exc:
            embed = discord.Embed(
                color=discord.Color.dark_theme(),
                title='{} Error Occured'.format(self.emojis['cross']),
                description='```yaml\n{}```'.format(exc)
            )

            await ctx.message.add_reaction('❎')
            await ctx.message.reply(embed=embed, mention_author=False)

    def finder(self, text, collection, *, key=None, lazy=True):
        suggestions = []
        text = str(text)
        pat = ".*?".join(map(re.escape, text))
        regex = re.compile(pat, flags=re.IGNORECASE)
        for item in collection:
            to_search = key(item) if key else item
            r = regex.search(to_search)
            if r:
                suggestions.append((len(r.group()), r.start(), item))

        def sort_key(tup):
            if key:
                return tup[0], tup[1], key(tup[2])
            return tup

        if lazy:
            return (z for _, _, z in sorted(suggestions, key=sort_key))
        else:
            return [z for _, _, z in sorted(suggestions, key=sort_key)]

    def parse_object_inv(self, stream, url):
        result = {}

        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        stream.readline().rstrip()[11:]
        stream.readline().rstrip()[11:]

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError(
                "Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(
            r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            async with aiohttp.ClientSession() as session:
                async with session.get(page + "/objects.inv") as resp:
                    if resp.status != 200:
                        raise RuntimeError(
                            "Cannot build rtfm lookup table, try again later."
                        )

                    stream = SphinxObjectFileReader(await resp.read())
                    cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            "latest": "https://discordpy.readthedocs.io/en/latest",
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, "_rtfm_cache"):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        cache = list(self._rtfm_cache[key].items())

        self.matches = self.finder(
            obj, cache, key=lambda t: t[0], lazy=False)[:8]

        embed = discord.Embed(color=discord.Color.dark_theme())
        if len(self.matches) == 0:
            return await ctx.send("Could not find anything. Sorry.")

        embed.description = "\n".join(
            f"[`{key}`]({url})" for key, url in self.matches)
        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command(
        name="Rtfm",
        description="Gives you a documentation link for a discord.py entity.",
        aliases=["Rtfd"],
        hidden=True
    )
    async def rtfm(self, ctx, *, query: str):
        key = "latest"
        await self.do_rtfm(ctx, key, query)


def setup(bot):
    bot.add_cog(Admin(bot))
