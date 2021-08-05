import discord
from discord.ext import buttons


class Pag(buttons.Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


def clean_code(content):
    """Automatically removes code blocks from the code."""

    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content
