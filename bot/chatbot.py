import asyncio
import socket
import datetime
from colorama import Fore,init

init(autoreset=True)
class ConnecTwitchChatBot:
    def __init__(self,streamer:str,oauth:str,botname:str) -> None:
        self.botname = botname
        self.streamer = streamer.lower()
        self.oauth = oauth
        self.socket = socket.socket()
        self.socket.connect(("irc.chat.twitch.tv",6667))
        
    async def connectTwitch(self):
        sends = [
            self.send(self.socket,f"PASS oauth:{self.oauth}"),
            self.send(self.socket,f"NICK {self.botname}"),
            self.send(self.socket,f"JOIN #{self.streamer}"),
            self.send(self.socket,f"CAP REQ :twitch.tv/tags"),
            self.send(self.socket,f"CAP REQ :twitch.tv/commands")
        ]
        await asyncio.gather(*sends)
        return await self.__run()

    async def send(self,socket:socket.socket,msg:str):
        return socket.send(bytes(msg+"\n","utf-8"))

    async def recv(self,socket:socket.socket):
        return socket.recv(4096).decode('utf-8')

    async def __run(self) -> None:
        if await self.recv(self.socket) != '' or await self.recv(self.socket) != None:
            while True:
                try:
                    msg = await self.recv(self.socket)
                    # print(msg)
                    parse = self.__messageParse(msg.replace("\n",''))
                    print(f"[{str(datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp())).split(chr(32))[1]}] ~ {parse['name']}{Fore.YELLOW} >>>{Fore.LIGHTYELLOW_EX} {parse['msg']}")
                    # await self.__chatCommands(parse["msg"])
                except (IndexError,TypeError):
                    pass
                except TimeoutError:
                    print("Zaman aşımı Gerçekleşti! Yeniden dene")
                except (ConnectionAbortedError,ConnectionResetError):
                    print(f"{Fore.RED}Bağlantıda Sorun algılandı! Yeniden dene")
                    break
    
    def __messageParse(self,msg:str) -> dict[str,str]:
        mod = False
        sub = False
        return_data = {}
        try:
            parse_tag = msg.split(";")
            parse_data = {}
            for i in range(len(parse_tag)):
                for j in range(len(parse_tag[i])):
                    if parse_tag[i][j] == '=':
                        parse_data.update({parse_tag[i][0:j] : parse_tag[i][j+1:len(parse_tag[i])]})

            type_ = parse_data["user-type"].split(f"#{self.streamer} :")
            parse_data["user-type"] = {"MESSAGE":type_[1]}

            if "moderator/1" in parse_data["badges"]:
                mod = True

            if parse_data["subscriber"] == '1':
                sub = True
                           
            if mod:
                return_data.update({ "name" : f"[{Fore.GREEN}MOD{Fore.RESET}]{'':<4}{Fore.GREEN}{parse_data['display-name']}", "msg" : f"{parse_data['user-type']['MESSAGE']}"})
                return return_data

            if sub:
                return_data.update({ "name" : f"[{Fore.LIGHTRED_EX}ABONE{Fore.RESET}]{'':<2}{Fore.LIGHTRED_EX}{parse_data['display-name']}", "msg" : f"{parse_data['user-type']['MESSAGE']}"})
                return return_data

            if not sub or not mod:
                return_data.update({ "name" : f"[{Fore.CYAN}PLEB{Fore.RESET}]{'':<3}{Fore.CYAN}{parse_data['display-name']}", "msg" : f"{parse_data['user-type']['MESSAGE']}"})
                return return_data
        except KeyError:
            pass
    
    # async def __chatCommands(self,msg:str):
    #     # print("msg",msg)
    #     if msg.startswith():
    #             await self.send(self.socket,f"PRIVMSG #{self.streamer} : /me sa")