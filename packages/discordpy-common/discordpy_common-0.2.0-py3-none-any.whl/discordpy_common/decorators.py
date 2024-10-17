import discord as ds
from discord.ext import commands

from collections.abc import Callable
from typing import Any
from enum import Enum

from _discord.bot import TypeDB

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)


class AuthType(Enum) :
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    PREMIUM = 'premium'
    USER = 'user'
    ...


# Verify in files
async def _file_auth(
        *,
        auth: AuthType,
        guild_id: str,
        member_id: str,
        **_
) -> bool :
    ...


# Verify in MongoDB
async def _mongo_auth(
        *,
        client: AsyncIOMotorClient,
        guild_id: str,
        member_id: str,
        auth: list[AuthType],
        **_
) -> bool :

    # Get the guild database
    guild_db: AsyncIOMotorDatabase = client.get_database(guild_id)
    if guild_db is None :
        return False

    # Get the authorized collection
    auth_collection = guild_db.get_collection('authorized')
    if auth_collection is None :
        return False

    # Check if the user or role is authorized
    user = await auth_collection.find_one({
        '_id': member_id,
        'auth': {
            '$in': [a.value for a in auth] + ['owner']
        }
    })
    if user is None :
        return False

    return True


# auth_only decorator
def auth_only(func: Callable[commands.Cog, ds.Interaction, tuple[Any, ...], dict[str, Any]], *auth: AuthType | None) -> Callable or None :
    """
    A decorator that checks if the user is authorized to execute the command
    :param func: `Callable` the command to execute
    :param auth: `AuthType` the authorization type. Default: `AuthType.ADMIN`
    :return:
    """

    # Define the different authentication modes
    auth_modes: dict[TypeDB, Callable] = {
        TypeDB.FILE : _file_auth,
        TypeDB.MONGO : _mongo_auth,
    }

    # Default auth type
    if auth is None :
        auth = [AuthType.ADMIN]

    async def wrapper(cog: commands.Cog, interaction: ds.Interaction, *args, **kwargs) -> Callable or None :

        # Verify if the user is authorized
        if not await auth_modes[cog.bot.typeDB](
                user_id=interaction.user.id.__str__(),
                guild_id=interaction.guild_id.__str__(),
                client=cog.bot.client,
                auth=auth,
        ) :
            await interaction.response.send_message('You are not authorized to do this !', ephemeral=True)
            return

        # Execute the command
        return func(cog, interaction, *args, **kwargs)

    return wrapper
