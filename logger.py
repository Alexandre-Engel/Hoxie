from datetime import datetime, timezone
import functools


def writeLog(message):
    time_ = datetime.now()
    now = "[" + time_.strftime("%d/%m/%Y %H:%M:%S") + "]: "
    logText = now + message
    logFile = open("discord.log", "a")
    logFile.write(logText + "\n")
    logFile.close()
    print(logText)


def writeLogCommand(command_func):
    @functools.wraps(command_func)
    async def logger(*args, **kwargs):
        writeLog(f"Commande {command_func.__name__} appellée")
        return await command_func(*args, **kwargs)

    return logger
