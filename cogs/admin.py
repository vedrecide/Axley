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
    async def _eval(self, ctx, *, code):
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
                result = f'{stdout.getvalue()}\n-- {obj}\n'
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

def setup(bot):
    bot.add_cog(Admin(bot))