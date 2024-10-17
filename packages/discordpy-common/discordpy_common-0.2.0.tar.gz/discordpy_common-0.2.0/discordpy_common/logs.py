from datetime import datetime
from enum import Enum


class LogType(Enum) :

    INFO = '[INFO]'
    ERROR = '[ERROR]'


class _GuildCreated :

    log_type: LogType
    date: str
    message: str

    def __init__(self, guild_id: str, date: datetime) -> None :
        log_type = LogType.INFO
        date = date.strftime('[%Y-%m-%d] [%H-%M-%S]')
        message = f'{date} [{log_type.value()}] Guild {guild_id} created. \n'


class Log(Enum) :

    GUILD_CREATED = _GuildCreated

    # Create a log
    def __call__(self, *args, **kwargs) :
        return self.value(*args, **kwargs)
