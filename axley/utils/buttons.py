import discord
import asyncio

from typing import List, Optional, Union
from discord.ext import commands
from discord_slash.utils.manage_components import (
    create_button,
    create_actionrow,
    ButtonStyle,
    wait_for_component,
)


class ButtonPaginator:
    def __init__(
        self,
        client: Union[discord.Client, commands.Bot],
        basic: Optional[List[Union[discord.Emoji, discord.PartialEmoji, str]]] = [
            "Previous",
            "Next",
        ],
        extra: Optional[List[Union[discord.Emoji, discord.PartialEmoji, str]]] = [
            "Initial",
            "Last",
        ],
    ) -> None:
        self.client = client
        self.basic = basic
        self.extra = extra
        self.left = str(self.basic[0])
        self.left2 = str(self.extra[0])
        self.right = str(self.basic[1])
        self.right2 = str(self.extra[1])
        self.page = 1

        if self.client == discord.Client:
            print(
                "<discord.Client> detected. It is highly recommended to use <discord.ext.commands.Bot>."
            )

        if self.basic:
            if isinstance(self.basic[0], discord.Emoji):
                self.left = discord.PartialEmoji(
                    name=self.basic[0].name,
                    animated=self.basic[0].animated,
                    id=self.basic[0].id,
                )
            if isinstance(self.basic[1], discord.Emoji):
                self.left = discord.PartialEmoji(
                    name=self.basic[1].name,
                    animated=self.basic[1].animated,
                    id=self.basic[1].id,
                )

        if self.extra:
            if isinstance(self.extra[0], discord.Emoji):
                self.left = discord.PartialEmoji(
                    name=self.extra[0].name,
                    animated=self.extra[0].animated,
                    id=self.extra[0].id,
                )
            if isinstance(self.extra[1], discord.Emoji):
                self.left = discord.PartialEmoji(
                    name=self.extra[1].name,
                    animated=self.extra[1].animated,
                    id=self.extra[1].id,
                )

    async def run(
        self,
        context: commands.Context,
        embeds=None,
        timeout=60,
        show_pages=False,
        use_extra_buttons=False,
    ):
        if not embeds:
            raise TypeError("Embeds cannot be None.")

        if len(embeds) < 2:
            raise TypeError("Embeds must be 2 or more.")

        async def generate_buttons(show_pages=False, use_extra_buttons=False):
            components = [
                create_button(style=ButtonStyle.green, label=self.left),
                create_button(style=ButtonStyle.green, label=self.right),
            ]
            if use_extra_buttons:
                components = [
                    create_button(style=ButtonStyle.green, label=self.left2),
                    create_button(style=ButtonStyle.green, label=self.left),
                    create_button(style=ButtonStyle.green, label=self.right),
                    create_button(style=ButtonStyle.green, label=self.right2),
                ]
            if show_pages:
                pos = len(components) // 2
                components.insert(
                    pos,
                    create_button(
                        style=ButtonStyle.red,
                        label="Page {}/{}".format(self.page, len(embeds)),
                        disabled=True,
                    ),
                )
            components = create_actionrow(*components)
            return components

        buttons = await generate_buttons(show_pages, use_extra_buttons)
        if use_extra_buttons:
            buttons["components"][0]["disabled"] = True

        msg = await context.send(embed=embeds[0], components=[buttons])
        component_labels = [self.left, self.right]
        if use_extra_buttons:
            component_labels = [self.left2, self.left, self.right, self.right2]

        while True:
            try:
                inter = await wait_for_component(
                    self.client,
                    components=buttons,
                    check=lambda i: i.component["label"] in component_labels and i.origin_message_id == msg.id and i.author.id == context.author.id,
                    timeout=int(timeout),
                )
                await inter.defer(edit_origin=True)
                if use_extra_buttons:
                    if inter.component["label"] == self.left2:
                        self.page = 1
                        buttons = await generate_buttons(show_pages, use_extra_buttons)
                        if self.page == 1:
                            buttons["components"][0]["disabled"] = True
                    elif inter.component["label"] == self.right2:
                        self.page = len(embeds)
                        buttons = await generate_buttons(show_pages, use_extra_buttons)
                        if self.page == len(embeds):
                            buttons["components"][-1]["disabled"] = True
                if inter.component["label"] == self.left:
                    if self.page == 1:
                        self.page = len(embeds)
                        buttons = await generate_buttons(show_pages, use_extra_buttons)
                        if use_extra_buttons:
                            buttons["components"][-1]["disabled"] = True
                    else:
                        self.page -= 1
                        buttons = await generate_buttons(show_pages, use_extra_buttons)
                    if use_extra_buttons:
                        if self.page == 1:
                            buttons["components"][0]["disabled"] = True
                elif inter.component["label"] == self.right:
                    if self.page == len(embeds):
                        self.page = 1
                        buttons = await generate_buttons(show_pages, use_extra_buttons)
                        if use_extra_buttons:
                            buttons["components"][0]["disabled"] = True
                    else:
                        self.page += 1
                        buttons = await generate_buttons(show_pages, use_extra_buttons)
                    if use_extra_buttons:
                        if self.page == len(embeds):
                            buttons["components"][-1]["disabled"] = True
                await inter.edit_origin(
                    embed=embeds[self.page - 1], components=[buttons]
                )
            except asyncio.TimeoutError:
                buttons = await generate_buttons(show_pages, use_extra_buttons)
                for t in buttons["components"]:
                    t["disabled"] = True
                await msg.edit(embed=embeds[self.page - 1], components=[buttons])
                self.page = 1
                break
