import typing
import discord
from discord import app_commands
from discord.ext import commands
import config
import random

import os
from dotenv import load_dotenv

# Load our .env file
load_dotenv()


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    admin = app_commands.Group(name="admin", description="Admin commands")
    # Above, we declare a command Group, in discord terms this is a parent command
    # We define it within the class scope (not an instance scope) so we can use it as a decorator.
    # This does have namespace caveats but i don't believe they're worth outlining in our needs.

    @admin.command(name="add", description="Add a domain to a service.")
    async def add(
        self, interaction: discord.Interaction, service: str, domain: str
    ) -> None:
        """Add a domain to a service."""
        if await config.get_permission_status(service, interaction.user.id):
            # Check if there are multiple domains being added.
            if " " in domain:
                domains = domain.split(" ")
                responses = []
                for domain_ in domains:
                    responses.append(await config.add_domain(domain_, service))
            else:
                responses = [await config.add_domain(domain, service)]

            if (
                len(
                    f"Added domain(s) to {service}. Output: ```{', '.join(responses)}```"
                )
                > 2000
            ):
                return await interaction.response.send_message(
                    "The output is too long to send.", ephemeral=True
                )

            # Send the message to the user saying the service it was from and the domain.
            await interaction.response.send_message(
                f"Added domain(s) to {service}. Output: ```{', '.join(responses)}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @add.autocomplete(name="service")
    async def add_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(name="remove", description="Remove a domain from a service.")
    async def remove(
        self, interaction: discord.Interaction, service: str, domain: str
    ) -> None:
        """Remove a domain from a service."""

        if await config.get_permission_status(service, interaction.user.id):
            # Check if there are multiple domains being removed.
            if " " in domain:
                domains = domain.split(" ")
                responses = []
                for domain_ in domains:
                    responses.append(await config.remove_domain(domain_, service))
            else:
                responses = [await config.remove_domain(domain, service)]

            # Send the message to the user saying the service it was from and the domain.
            if (
                len(
                    f"Removed domain(s) from {service}. Output: ```{', '.join(responses)}```",
                )
                > 2000
            ):
                return await interaction.response.send_message(
                    "The output is too long to send.", ephemeral=True
                )

            await interaction.response.send_message(
                f"Removed domain(s) from {service}. Output: ```{', '.join(responses)}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @remove.autocomplete(name="service")
    async def remove_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="listall",
        description="List all domains from a service.",
    )
    async def listall(self, interaction: discord.Interaction, service: str) -> None:
        """List all domains from a service."""
        if await config.get_permission_status(service, interaction.user.id):
            domains = await config.get_domains(service)
            domains = ", ".join(domains)
            await interaction.response.send_message(
                f"Domains for {service}:\n```{domains}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @listall.autocomplete(name="service")
    async def listall_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(name="add_premium", description="Add a domain to a service.")
    async def add_premium(
        self, interaction: discord.Interaction, service: str, domain: str
    ) -> None:
        """Add a domain to a service."""
        if await config.get_permission_status(service, interaction.user.id):
            # Check if there are multiple domains being added.
            if " " in domain:
                domains = domain.split(" ")
                responses = []
                for domain_ in domains:
                    responses.append(await config.add_premium_domain(domain_, service))
            else:
                responses = [await config.add_premium_domain(domain, service)]

            # Send the message to the user saying the service it was from and the domain.
            await interaction.response.send_message(
                f"Added domain(s) to {service}. Output: ```{', '.join(responses)}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @add_premium.autocomplete(name="service")
    async def add_premium_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(name="remove_premium", description="Remove a domain from a service.")
    async def remove_premium(
        self, interaction: discord.Interaction, service: str, domain: str
    ) -> None:
        """Remove a domain from a service."""

        if await config.get_permission_status(service, interaction.user.id):
            # Check if there are multiple domains being removed.
            if " " in domain:
                domains = domain.split(" ")
                responses = []
                for domain_ in domains:
                    responses.append(
                        await config.remove_premium_domain(domain_, service)
                    )
            else:
                responses = [await config.remove_premium_domain(domain, service)]

            # Send the message to the user saying the service it was from and the domain.
            await interaction.response.send_message(
                f"Removed domain(s) from {service}. Output: ```{', '.join(responses)}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @remove_premium.autocomplete(name="service")
    async def remove_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="listall_premium",
        description="List all domains from a service.",
    )
    async def listall_premium(
        self, interaction: discord.Interaction, service: str
    ) -> None:
        """List all domains from a service."""
        if await config.get_permission_status(service, interaction.user.id):
            domains = await config.get_premium_domains(service)
            domains = ", ".join(domains)
            await interaction.response.send_message(
                f"Domains for {service}:\n```{domains}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @listall_premium.autocomplete(name="service")
    async def listall_premium_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="set_cooldown",
        description="Set the cooldown for a service.",
    )
    async def set_cooldown(
        self, interaction: discord.Interaction, service: str, max_uses: int, cooldown: int
    ) -> None:
        """Set the cooldown for a service."""
        if await config.get_permission_status(service, interaction.user.id):
            response1 = await config.set_service_max_uses(service, max_uses)
            response2 = await config.set_service_cooldown(service, cooldown)
            await interaction.response.send_message(
                f"Set cooldown for {service}. Output: ```{response1}, {response2}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @set_cooldown.autocomplete(name="service")
    async def set_cooldown_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data
    
    @admin.command(
        name="set_user_cooldown",
        description="Set the cooldown for a service.",
    )
    async def set_user_cooldown(
        self, interaction: discord.Interaction, user: discord.User, service: str, count: int
    ) -> None:
        """Set the cooldown for a service."""
        if await config.get_permission_status(service, interaction.user.id):
            response = await config.set_user_num_uses(user.id, service, count)
            await interaction.response.send_message(
                f"Set cooldown for {service}. Output: ```{response}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    @set_user_cooldown.autocomplete(name="service")
    async def set_user_cooldown_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="add_service",
        description="Add a service. (Only accessible if you have access to manage the main service)",
    )
    async def add_service(
        self, interaction: discord.Interaction, service: str, url: str, description: str
    ):
        main_service = await config.get_main_service()
        """Add a service to the proxy."""
        if not await config.get_permission_status(main_service, interaction.user.id):
            await interaction.response.send_message(
                "You don't have permission to do that!", ephemeral=True
            )
            return

        response = await config.add_service(service, url, description)
        await interaction.response.send_message(
            f"Added {service} to the proxy.\nResponse:\n```{response}```",
            ephemeral=True,
        )

    @admin.command(
        name="add_manager",
        description="Add a manager to a service. (Only accessible if you have access to manage the main service)",
    )
    async def add_manager(
        self, interaction: discord.Interaction, service: str, user: discord.User
    ):
        main_service = await config.get_main_service()
        """Add a manager to a service."""
        if not await config.get_permission_status(main_service, interaction.user.id):
            await interaction.response.send_message(
                "You don't have permission to do that!", ephemeral=True
            )
            return

        response = await config.add_manager(service, user.id)
        await interaction.response.send_message(
            f"Added {user} to {service}.\nResponse:\n```{response}```",
            ephemeral=True,
        )

    @add_manager.autocomplete(name="service")
    async def add_manager_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="remove_manager",
        description="Remove a manager from a service. (Only accessible if you have access to manage the main service)",
    )
    async def remove_manager(
        self, interaction: discord.Interaction, service: str, user: discord.User
    ):
        main_service = await config.get_main_service()
        """Remove a manager from a service."""
        if not await config.get_permission_status(main_service, interaction.user.id):
            await interaction.response.send_message(
                "You don't have permission to do that!", ephemeral=True
            )
            return

        response = await config.remove_manager(service, user.id)
        await interaction.response.send_message(
            f"Removed {user} from {service}.\nResponse:\n```{response}```",
            ephemeral=True,
        )

    @remove_manager.autocomplete(name="service")
    async def remove_manager_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="get_info",
        description="Get information about a service you manage.",
    )
    async def get_info(self, interaction: discord.Interaction, service: str):
        """Get information about a service you manage."""
        if await config.get_permission_status(service, interaction.user.id):
            data = await config.get_service_info(service)
            await interaction.response.send_message(
                f"Information about {service}:\n\n```{data}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You don't have permission to do that!", ephemeral=True
            )

    @get_info.autocomplete(name="service")
    async def get_info_service_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for service in await config.get_services():
            data.append(app_commands.Choice(name=service, value=service))
        return data

    @admin.command(
        name="set_password",
        description="Set the password for the main service.",
    )
    async def set_password(self, interaction: discord.Interaction, password: str):
        """Set the password for the main service."""
        main_service = await config.get_main_service()
        if await config.get_permission_status(main_service, interaction.user.id):
            response = await config.change_password(password)
            await interaction.response.send_message(
                f"Set the password for {main_service} to {password}.\n\nOutput: ```{response}```",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You don't have permission to do that!", ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot), guild=bot.get_guild(int(os.getenv("GUILD_ID"))))
