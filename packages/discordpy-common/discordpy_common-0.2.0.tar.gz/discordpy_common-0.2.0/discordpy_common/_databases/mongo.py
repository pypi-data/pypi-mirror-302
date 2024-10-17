from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi

from discordpy_common import Log

from datetime import datetime
import asyncio


# Override the AsyncIOMotorClient class
class Client(AsyncIOMotorClient) :

    main_db: AsyncIOMotorDatabase | None

    # Initialize the client and ping the server
    def __init__(self, uri: str) :
        super().__init__(uri, server_api=ServerApi('1'))
        asyncio.run(self._ping())
        self.main_db = None

    async def _ping(self) :

        # Check if the connection is successful
        try :
            await self.admin.command('ping')
            print('Pinged your deployment. You successfully connected to MongoDB !')

        except Exception as e :
            raise Exception('Could not connect to MongoDB', e)

    async def create_guild_db(self, guild_id: str, owner_id: str) -> None :

        # Create the guild database
        guild_db = self[guild_id]
        if auth_coll := guild_db.get_collection('authorized') is None :
            auth_coll = await guild_db.create_collection('authorized')

        # Insert the owner in the authorized collection
        await auth_coll.insert_one({
            '_id': owner_id,
            'auth': ['owner']
        })

        # Create the logs collection
        if logs_coll := guild_db.get_collection('logs') is None :
            logs_coll = await guild_db.create_collection('logs')

        # Get the number of logs for the current day
        nb_logs_day: int = len(await logs_coll.find({
            '_id': {
                '$regex': datetime.now().strftime('%Y-%m-%d')
            }}).to_list(None))

        # Create the guild created log
        date: datetime = datetime.now()
        guild_log: Log.GUILD_CREATED = Log.GUILD_CREATED(guild_id=guild_id, date=date)

        # Insert the log in the logs collection
        await logs_coll.insert_one({
            '_id': f'{date.strftime('%Y-%m-%d')}_{nb_logs_day}',
            'type': guild_log.log_type,
            'message': guild_log.message,
        })
