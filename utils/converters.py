from discord.ext import commands


class TimeConverter(commands.Converter):
    async def convert(self, ctx, arg):
        amount = arg[:-1]
        unit = arg[-1]

        if amount.isdigit() and unit in [
            's',
            'm',
            'h',
            'd',
            'w'
        ]:
            return (int(amount), unit)

        raise commands.BadArgument(
            message='''
                Duration is not valid!\nAnd it only supports till weeks or `w`
            '''
        )


class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(
                    f"{argument} is not a valid member or member ID."
                ) from None
        else:
            return m.id
