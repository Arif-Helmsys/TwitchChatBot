from bot import chatbot
from platform import python_version
import os
import pickle
import asyncio
from colorama import init,Fore,Style
from getpass import getuser

init(autoreset=True)
banner = f"""{Fore.LIGHTGREEN_EX}
  .,-:::::   ::   .:   :::. :::::::::::::::::::.      ...   ::::::::::::
,;;;'````'  ,;;   ;;,  ;;`;;;;;;;;;;'''' ;;;'';;'  .;;;;;;;.;;;;;;;;''''
[[[        ,[[[,,,[[[ ,[[ '[[,   [[      [[[__[[\\.,[[     \[[,   [[     
$$$        '$$$'''$$$c$$$cc$$$c  $$      $$''''Y$$$$$,     $$$   $$     
`88bo,__,o, 888   "88o888   888, 88,    _88o,,od8P"888,_ _,88P   88,
  "YUMMMMMP"MMM    YMMYMM   ""`  MMM    ""YUMMMP"   "YMMMMMP"    MMM
                                {Fore.LIGHTMAGENTA_EX}for Twitch
                Github:https://github.com/Arif-Helmsys
"""
async def main():
    print(banner)
    streamer = ""
    botname = ""
    oauth = ""
    branch = ""
    isClose = False
    while isClose != True:
        botname = input(f"{Fore.CYAN}╭──({Fore.LIGHTMAGENTA_EX}B0TNAME@{getuser().lower()}{Fore.CYAN})~{Fore.RED}[{Fore.CYAN}Botun Adı{Fore.RED}]{Fore.CYAN}\n╰──────{Fore.RED}# ")
        streamer = input(f"{Fore.CYAN}╭──({Fore.LIGHTMAGENTA_EX}STREAMER@{getuser().lower()}{Fore.CYAN})~{Fore.RED}[{Fore.CYAN}Kayıtlı yayıncı adı varsa boş geç{Fore.RED}]{Fore.CYAN}\n╰──────{Fore.RED}# ")
        if not os.path.exists("data.pickle"):
            oauth = input(f"{Fore.CYAN}╭──({Fore.LIGHTMAGENTA_EX}T0KEN@{getuser().lower()}{Fore.CYAN}){Fore.CYAN}\n╰──────{Fore.RED}# ")
            print(f"{Fore.CYAN}\t ╰───/{Fore.WHITE}Bir daha token girmemek adına tokeni kaydetmek istiyor musun ?\n".expandtabs(11))
            branch = input(f"{Fore.CYAN}╭──({Fore.LIGHTMAGENTA_EX}CHATB0T@{getuser().lower()}{Fore.CYAN})~{Fore.RED}[{Fore.CYAN}Y/n{Fore.RED}]{Fore.CYAN}\n╰──────{Fore.RED}# ")
        
        else:
            isClose = True

        if branch.lower() == 'y':
            writePickle(streamer,oauth)
            isClose = True

        if branch.lower() == "exit" or streamer.lower() == "exit":
            print(f"{Fore.CYAN}\t ╰───/{Fore.WHITE} Hoşçakal\n".expandtabs(11))
            exit(0)
    
    if isClose:
        if os.path.exists("data.pickle"):
            data = readPickle()
            streamer = data["streamer"]
            oauth = data["oauth"]
        os.system("cls||clear")
        print(streamer,oauth)
        bot = chatbot.ConnecTwitchChatBot(streamer,oauth,botname)
        return await bot.connectTwitch()

def writePickle(_streamer:str,_oauth:str):
    data = {
        "streamer":_streamer,
        "oauth":_oauth
    }
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def readPickle():
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        return data

if __name__ == "__main__":
    if float(str(python_version()[:3])) == 3.9:
        asyncio.run(main())