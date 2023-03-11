import typing
import discord
from discord import app_commands
from discord.ext import commands
import config
import random
import datetime

import os
from dotenv import load_dotenv

# Load our .env file
load_dotenv()


class Premium(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    premium = app_commands.Group(name="premium", description="Premium proxy commands")
    # Above, we declare a command Group, in discord terms this is a parent command
    # We define it within the class scope (not an instance scope) so we can use it as a decorator.
    # This does have namespace caveats but i don't believe they're worth outlining in our needs.

    @premium.command(
        name="get",
        description="Get a premium proxy url, choose from the following services given.",
    )
    async def get(self, interaction: discord.Interaction, service: str) -> None:
        """Get a proxy url, choose from the following services given."""

        # Check if the user is on cooldown.
        usable, response = await config.get_cooldown(str(interaction.user.id), service + "_premium")
        service_cooldown = await config.get_service_cooldown(service)
        if not usable:
            return await interaction.response.send_message(
                f"Error: {response}.", ephemeral=True
            )

        # Check if there are any domains for the service.
        if len(await config.get_premium_domains(service)) == 0:
            return await interaction.response.send_message(
                f"There are no domains for {service}.", ephemeral=True
            )

        # Grab a random domain from the list of domains for the service.
        domain = random.choice(await config.get_premium_domains(service))

        # Send the message to the user saying the service it was from and the domain.
        await interaction.response.send_message(
            f"Randomly choosen premium domain from {service}: `{domain}`", ephemeral=True
        )
        await config.set_cooldown(str(interaction.user.id), service_cooldown, service + "_premium")
        await config.service_counter(service, 1)

    @get.autocomplete(name="service")
    async def get_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @premium.command(name="get_pass", description="Get the password for a service.")
    async def get_pass(self, interaction: discord.Interaction) -> None:
        """Get the password for a service."""
        await interaction.response.send_message(
            f"Username: `discord`\nPassword: `{await config.get_password()}`",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Premium(bot), guild=bot.get_guild(int(os.getenv("GUILD_ID"))))
