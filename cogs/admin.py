import discord, textwrap, io, contextlib

from discord.ext import commands
from .utils.paginator import clean_code
from .utils.paginator import Pag
from traceback import format_exception

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis

    @commands.command(name='Eval', description='Evaluates a Python code')
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        code = clean_code(code)

        local_variables = {
            'discord': discord,
            'commands': commands,
            'self': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f'async def func():\n{textwrap.indent(code,"    ")}', local_variables,
                )

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

    @commands.command(name='Reload', description='Reloads a cog..')
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.reload_extension(f'{cog}')
            embed = discord.Embed(
                color=discord.Color.dark_theme(),
                description='{} Successfully reloaded `{}`'.format(self.emojis['tick'], cog)
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


def setup(bot):
    bot.add_cog(Admin(bot))