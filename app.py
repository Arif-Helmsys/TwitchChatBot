from bot import chatbot
from platform import python_version
from os import system
import asyncio

async def main():
    streamer = input("Yayıncı >>> ")
    oauth = input("Token >>> ")
    system("cls||clear")
    bot = chatbot.ConnecTwitchChatBot(streamer,oauth)
    return await bot.connectTwitch()

if __name__ == "__main__":
    if float(str(python_version()[:3])) == 3.9:
        asyncio.run(main())