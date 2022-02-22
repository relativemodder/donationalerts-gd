import gd
import asyncio
from donationalerts_api.asyncio_api import Alert
from time import sleep
import win32gui

from random import randint as rand

print("Welcome to the donationalerts-gd!\nYou can change settings in config file.\nNote: 10 RUB does the same thing as 10 USD or 10 EUR\nPress enter...")
input()
config = {
    'alerts_token': '',
    'amount_kill': '',
    'amount_freeze': '',
    'amount_speedup': '',
    'amount_speeddown': '',
    'amount_resize': '',
    'amount_everything_hurts': '',
    'amount_resize_win': ''
}

def parseConfig(config_raw:str):
    global config
    lines = config_raw.splitlines()
    for line in lines:
        l = line.replace(" ", "")
        p = l.split("=")
        k = p[0]
        v = p[1]
        config[k]=str(v)
    print("Config have been parsed!")
f = open("config", "r")
txt = f.read(99999)
parseConfig(txt)
f.close()
alert = Alert(config["alerts_token"])

memory = gd.memory.get_memory()

print("Ready to listen donationalerts socket")
print("Listening for donates...")
@alert.event()
async def handler(event):
    global memory
    print(f"{event.username} donated {event.amount_formatted} {event.currency} | {event.message}")
    if(str(event.amount_formatted)==config["amount_kill"]):
        memory.player_kill()
        print("Kill")
    if(str(event.amount_formatted)==config["amount_freeze"]):
        memory.player_freeze()
        print("Freeze")
        sleep(4)
        memory.player_unfreeze()
        print("Unreeze")
    if(str(event.amount_formatted)==config["amount_speedup"]):
        memory.set_speed_value(4.2)
        print("Speedup")
    if(str(event.amount_formatted)==config["amount_speeddown"]):
        memory.set_speed_value(0.3)
        print("Speeddown")
    if(str(event.amount_formatted)==config["amount_resize"]):
        memory.set_size(0.2)
        print("Resize")
    if(str(event.amount_formatted)==config["amount_resize_win"]):
        hwnd = win32gui.FindWindow(None, 'Geometry Dash')
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        w = x1 - x0
        h = y1 - y0
        win32gui.MoveWindow(hwnd, x0, y0, rand(400, 1280), rand(100, 720), True)
        print("Window resized")
    if(str(event.amount_formatted)==config["amount_everything_hurts"]):
        memory.write_bytes(gd.memory.Buffer[0xB8, 0x02, 0x00, 0x00, 0x00, 0x90], 0x20456D)
        print("Everything hurts")
        sleep(4)
        memory.write_bytes(gd.memory.Buffer[0x8B, 0x83, 0x00, 0x03, 0x00, 0x00], 0x20456D)
        print("Everything doesn't hurt")
