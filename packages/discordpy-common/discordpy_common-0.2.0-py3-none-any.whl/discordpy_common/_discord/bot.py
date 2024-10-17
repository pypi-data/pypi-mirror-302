import discord as ds
from discord.ext import commands

from enum import Enum
import asyncio
import os

from discordpy_common import (
    Client as mongoClient,
    base_architecture,
)

from motor.motor_asyncio import AsyncIOMotorDatabase


# Type aliases
type DBClient = mongoClient
type DB = AsyncIOMotorDatabase


# Intents
class Intents(ds.Intents) :
    pass


# Database types / Storage types
class TypeDB(Enum) :
    """
    Enum class that defines the different types of databases
    """
    FILE = 1
    MONGO = 2
    ...


# Override the Bot class
class Bot(commands.Bot) :

    _token: str
    typeDB: TypeDB
    client: DBClient
    db_name: str

    def __init__(
            self,
            *,
            token: str,
            prefix: str,
            desc: str,
            intents: Intents | None = Intents.all(),
            typeDB: TypeDB,
            cogs_dir: str | None = None,
            remove_help: bool = True,
            connection_string: str | None = None,
            db_name: str | None = None,
            **kwargs,
    ) -> None :

        # Initialize the bot
        super().__init__(command_prefix=prefix, description=desc, intents=intents, **kwargs)
        self._token = token
        self.db = typeDB
        self.db_name = db_name

        # Connect to the database
        if self.db != TypeDB.FILE :
            if connection_string is None :
                raise ValueError('You must provide a connection string for the database')

            self._connect_to_db(connection_string)

        # Create file architecture
        else :
            base_architecture()

        # Remove the help command
        self.remove_command('help') if remove_help else None
        # Start the bot
        asyncio.run(self._start_bot(token, cogs_dir))

    async def _load(self, cogs_dir: str) -> None :

        # Verify if the directory exists
        if not os.path.exists(cogs_dir) :
            raise FileNotFoundError(f'{cogs_dir} does not exist')

        # Load the cogs
        for file_name in os.listdir(cogs_dir) :
            if file_name.endswith('.py') :
                await self.load_extension(
                    f'{cogs_dir}.{file_name[:-3]}'
                    .replace('/', '.')
                    .replace('\\', '.')
                )
        print('Cogs loaded !')

    async def _start_bot(self, token: str, cog_dir: str | None = './cogs') -> None :

        # Load the cogs and start the bot
        if cog_dir is not None :
            await self._load(cog_dir)
        await super().start(token)

    def _connect_to_db(self, connection_string: str) -> None :

        # Define the connection modes
        connect_modes: dict[TypeDB, callable] = {
            TypeDB.MONGO : self._mongodb_connect,
        }
        # Connect to the database
        return connect_modes[self.typeDB](connection_string)

    def _mongodb_connect(self, connection_string: str) -> None :

        # Create client
        self.client: mongoClient = mongoClient(connection_string)

        # Connect to the default database
        if self.db_name is None :
            self.client.main_db = self.client.get_default_database()

            if self.client.main_db is None :
                raise ValueError('No database found')
            print(f'Connected to the default database: {self.client.main_db.name}')
            return

        # Connect to the specified database
        self.client.main_db = self.client.get_database(self.db_name)

        if self.client.main_db is None :
            raise ValueError(f'No database found with name {self.db_name}')
        print(f'Connected to the database: {self.client.main_db.name}')
