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


class Proxy(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    proxy = app_commands.Group(name="proxy", description="Proxy commands")
    # Above, we declare a command Group, in discord terms this is a parent command
    # We define it within the class scope (not an instance scope) so we can use it as a decorator.
    # This does have namespace caveats but i don't believe they're worth outlining in our needs.

    @proxy.command(
        name="get",
        description="Get a proxy url, choose from the following services given.",
    )
    async def proxy_command(self, interaction: discord.Interaction, service: str) -> None:
        """Get a proxy url, choose from the following services given."""

        async def log(log_message: str):
            """Log a message to a specific channel."""
            channel = self.bot.get_channel(int(os.getenv("LOG_CHANNEL")))
            await channel.send(log_message)

        # Check to see if the service is valid.
        if service not in await config.get_services():
            return await interaction.response.send_message(
                f"Error: {service} is not a valid service.", ephemeral=True
            )

        # Check if the user is on cooldown.
        usable, response = await config.get_cooldown(service, str(interaction.user.id))
        service_cooldown = await config.get_service_cooldown(service)
        if not usable:
            return await interaction.response.send_message(
                f"Error: {response}.", ephemeral=True
            )

        # Check if there are any domains for the service.
        domains = await config.get_domains(service)
        if len(domains) == 0:
            await log(
                f"User: {interaction.user.id}\nThere are no domains for {service}."
            )
            return await interaction.response.send_message(
                f"There are no domains for {service}.", ephemeral=True
            )

        # Grab a random domain from the list of domains for the service.
        domain = random.choice(domains)

        # Check if the domain has been accessed before by grabbing the users history
        # and checking if the domain is in it. If it is, we'll grab a new domain.
        # However if the user has grabbed all the domains for the service, we'll
        # send an error message.
        while domain in await config.get_history(service, str(interaction.user.id)):
            if len(domains) == len(
                await config.get_history(service, str(interaction.user.id))
            ):
                await interaction.response.send_message(
                    f"There are no more domains for {service}. Please wait as the admin restocks domains.",
                    ephemeral=True,
                )
                return await log(
                    f"User: {interaction.user.id}\nThere are no more domains for {service}."
                )
            domain = random.choice(domains)

        # Send the message to the user saying the service it was from and the domain.
        await interaction.response.send_message(
            f"Randomly choosen domain from {service}: `{domain}`", ephemeral=True
        )
        await config.log_history(service, str(interaction.user.id), domain)
        await config.set_cooldown(str(interaction.user.id), service_cooldown, service)
        await config.service_counter(service, 1)
        await log(
            f"User: {interaction.user.id}\nUsed the {service} proxy command. Domain: {domain}."
        )

    @proxy_command.autocomplete(name="service")
    async def proxy_command_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @proxy.command(
        name="history",
        description="Get your history of domains you've used.",
    )
    async def proxy_history(self, interaction: discord.Interaction, service: str) -> None:
        """Get your history of domains you've used."""

        if service not in await config.get_services():
            return await interaction.response.send_message(
                f"Error: {service} is not a valid service.", ephemeral=True
            )

        history = await config.get_history(service, str(interaction.user.id))
        if len(history) == 0:
            return await interaction.response.send_message(
                f"You have no history for {service}.", ephemeral=True
            )
        await interaction.response.send_message(
            f"Your history for {service}: {', '.join(history)}", ephemeral=True
        )
        
    @proxy_history.autocomplete(name="service")
    async def proxy_history_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Proxy(bot), guild=bot.get_guild(int(os.getenv("GUILD_ID"))))
