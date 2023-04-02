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
        usable, response = await config.get_cooldown(
            service + "_premium", str(interaction.user.id)
        )
        service_cooldown = await config.get_service_cooldown(service)
        if not usable:
            await log(f"User: {interaction.user.id}\nError: {response}.")
            return await interaction.response.send_message(
                f"Error: {response}.", ephemeral=True
            )

        # Check if there are any domains for the service.
        if len(await config.get_premium_domains(service)) == 0:
            await log(
                f"User: {interaction.user.id}\nThere are no domains for {service}."
            )
            return await interaction.response.send_message(
                f"There are no domains for {service}.", ephemeral=True
            )

        # Grab a random domain from the list of domains for the service.
        domain = random.choice(await config.get_premium_domains(service))

        # Check if the domain has been accessed before by grabbing the users history
        # and checking if the domain is in it. If it is, we'll grab a new domain.
        # However if the user has grabbed all the domains for the service, we'll
        # send an error message.
        while domain in await config.get_history(
            service + "_premium", str(interaction.user.id)
        ):
            if len(await config.get_premium_domains(service)) == len(
                await config.get_history(service + "_premium", str(interaction.user.id))
            ):
                await interaction.response.send_message(
                    f"There are no more premium domains for {service}. Please wait as the admin restocks domains.",
                    ephemeral=True,
                )
                return await log(
                    f"User: {interaction.user.id}\nThere are no more domains premium for {service}."
                )
            domain = random.choice(await config.get_premium_domains(service))

        # Send the message to the user saying the service it was from and the domain.
        await interaction.response.send_message(
            f"Randomly choosen premium domain from {service}: `{domain}`",
            ephemeral=True,
        )
        await config.log_history(service + "_premium", str(interaction.user.id), domain)
        await config.set_cooldown(
            str(interaction.user.id), service_cooldown, service + "_premium"
        )
        await config.service_counter(service, 1)
        await log(
            f"User: {interaction.user.id}\nGot a premium proxy from {service}. Domain: {domain}"
        )

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

        async def log(log_message: str):
            """Log a message to a specific channel."""
            channel = self.bot.get_channel(int(os.getenv("LOG_CHANNEL")))
            await channel.send(log_message)

        await interaction.response.send_message(
            f"Username: `discord`\nPassword: `{await config.get_password()}`",
            ephemeral=True,
        )
        await log(f"User: {interaction.user.id} got the password.")

    @premium.command(
        name="history",
        description="Get your history for a service, if no service is given, it will return all your history.",
    )
    async def premium_history(
        self, interaction: discord.Interaction, service: str
    ) -> None:
        """Get your history of domains you've used."""

        history = await config.get_history(service + "_premium", str(interaction.user.id))
        if len(history) == 0:
            return await interaction.response.send_message(
                f"You have no premium history for {service}.", ephemeral=True
            )
        await interaction.response.send_message(
            f"Your premium history for {service}: {', '.join(history)}", ephemeral=True
        )

    @premium_history.autocomplete(name="service")
    async def proxy_history_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Premium(bot), guild=bot.get_guild(int(os.getenv("GUILD_ID"))))
