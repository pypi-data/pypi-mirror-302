class progress:
 import os
 from colorama import Fore, Back, Style
 import time
 import asyncio
 def __init__(self):
   pass
 @staticmethod
 async def clear():
   self=progress()
   self.os.system('cls' if self.os.name == 'nt' else 'clear')
 @staticmethod
 def start(title: str):
  self=progress()
  print(f"\r{self.Fore.WHITE}{title}({self.Fore.BLACK}❚❚❚❚❚❚❚❚❚❚{self.Fore.WHITE}) {self.Fore.BLACK}- {self.Fore.WHITE}0%",end="")
 @staticmethod
 def setprecent(title: str, amo, oof):
  amount=int((amo/oof)*100)
  def prt(prg, amo, oof):
    self=progress()
    if amo == oof:
        print(f"\r{self.Fore.WHITE}{title}{self.Fore.WHITE}({self.Fore.WHITE}❚❚❚❚❚❚❚❚❚❚) - 100%  {oof}/{oof} {self.Fore.GREEN}✓{self.Fore.WHITE}")
    else:
        print(f"\r{self.Fore.WHITE}{title}{self.Fore.WHITE}(" + ((f"{self.Fore.WHITE}❚" * int(prg / 10)) + f"{self.Fore.BLACK}❚" * int(10 - int(prg / 10))) + f"{self.Fore.WHITE}) {self.Fore.BLACK}- " + f"{self.Fore.WHITE}{prg}%  {amo}/{oof}", end="")
  prt(amount, amo, oof)
