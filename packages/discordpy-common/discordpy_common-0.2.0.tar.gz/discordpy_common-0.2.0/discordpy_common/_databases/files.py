from datetime import datetime
import os

from discordpy_common import Log


# Global directories paths
_base_directories: list[str] = [
    './src',
    '.src/guilds',
]

# Guild directory paths
_guild_directories: list[str] = [
    './src/guilds/{guild_id}',
    './src/guilds/{guild_id}/logs',
    './src/guilds/{guild_id}/authorized',
    './src/guilds/{guild_id}/temp',
]

# Guild files paths
_guild_files: list[str] = [
    './src/guilds/{guild_id}/authorized/admin.txt',
    './src/guilds/{guild_id}/logs/{date}.txt',
    './src/guilds/{guild_id}/temp/temp.txt',
]


def base_architecture() -> None :

    # Create all directories if not exist
    for directory in _base_directories :
        if not os.path.exists(directory) :
            os.mkdir(directory)
            print(f'Created {directory}')
        else :
            print(f'{directory} already exists')
    print('Architecture created !')


def create_guild_pattern(guild_id: str) -> None :
    """
    Create files and directories used by a guild
    :param guild_id: `str` the guild id
    :return:
    """

    # Create all directories if not exist
    for directory in _guild_directories :
        # Replace with current guild id
        directory = directory.format(guild_id=guild_id)
        if not os.path.exists(directory) :
            os.mkdir(directory)

    # Get current datetime
    date: datetime = datetime.now()
    ymd_format: str = date.strftime('%Y-%m-%d')

    # Create all files if not exist
    for file in _guild_files :
        # Replace with current guild and date
        file = file.format(guild_id=guild_id, date=ymd_format)
        if not os.path.exists(file) :
            with open(file, 'w', encoding='UTF-8') as f :
                f.write('')

    # Write a message in logs
    with open(f'.src/guilds/{guild_id}/logs/{ymd_format}.txt', 'a+', encoding='UTF-8') as f :
        f.write(Log.GUILD_CREATED(guild_id=guild_id, date=date).message)
