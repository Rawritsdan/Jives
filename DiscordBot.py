"""
 sudo python3.4 ./DiscordBot.py
 Python 3.5 has very serious changes, < Python 3.4 is no longer supported :(

The first yield from command is always flagged as broken..it's fine shh.
#print (dir(message.message)) #View object attributes, useful for seeing where data sits

Todo:
    Add betting #Dicks
    Finish Aliases
    Set Game to RL on Sundays
    New Joined channel info to console and log https://rapptz.github.io/discord.py/api.html#discord.Channel
    Get last message, randomly say 1 in 30 or so times [Quote} - allegedly]
"""

import discord
import asyncio
from discord.ext import commands
import sys
import random
import logging
import subprocess
import traceback
import datetime

global Admins
#global TrainsMissed
global Settings
Admins = '/home/pi/bin/Python/DiscordAdmins.txt'
SettingsFileLoc = '/home/pi/bin/Python/DiscordBotSettings.txt'
global VoiceChannelsActive
VoiceChannelsActive = []

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='/home/pi/bin/Python/DiscordBot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

def GetSettings(Setting):
    try:
        Settings = {}
        with open(SettingsFileLoc) as SettingsFile:
            SettingsSTR = SettingsFile.read().splitlines( )
        SettingsFile.close
        for InSettings in SettingsSTR: #Split into key pairs
            print ("=== Generating Settings ===")
            SettingsData = InSettings.split("=") #Split individually
            print ("Var Name: {0}".format(SettingsData[0]))
            print ("Var Value: {0}".format(SettingsData[1]))
            VarName=SettingsData[0]
            VarValue=SettingsData[1]
            Settings.update({VarName:VarValue})
            #Settings[VarName] = VarValue #Python 2 not Python 3
            print ("=== Completed Generating Settings ===")
        print ("All Vars: {0}".format(Settings))
    except IndexError:
        print ("No Setting Found in {0}").format(SettingsFile)
    return Settings[Setting]

def CommandRun(user,command): #Log commands run.
    fmt =""">Command Received: {1}\n  -From: {0}""".format(user,command)
    print (fmt)
    LogFileFMT = "[{0}] >Command Received: '{2}' from: {1}".format(datetime.datetime.now(),user,command)
    discord_logger.info(LogFileFMT)

def AdminCheck(user):
    print("------")
    print ("Checking For Admin...")
    #print ("Author: ",user)
    with open(Admins) as AdminFile:
            lines = AdminFile.read().splitlines( )
    AdminFile.close
    #print("Admins:",lines)
    user = str(user)
    IsAdmin = user in lines
    print ("Is User Admin: "+(str(IsAdmin)))
    LogFileFMT = "[{0}] Admin Check for user '{1}' returned: {2}".format(datetime.datetime.now(),user,IsAdmin)
    discord_logger.info(LogFileFMT)
    return IsAdmin

class Commands:
    def __init__(self, bot):
        self.bot = bot #Give it 'passthrough', can't call bot if bot hasn't been defined until later
        self.player = None
        self.voice = None #Because of this, don't use the function name 'Voice' it will disappear

    @commands.command(pass_context=True, no_pm=False,aliases=['Rocket League', 'RocketLeague', 'RL','rocketleague']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def rl(self,message):
        """- Show RL server details"""
        fmt = """\nRocket League Server Details:\nUsername: CGAYYY\nPassword: buildissue"""
        yield from self.bot.say(fmt)
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="Game",pass_context=True, no_pm=False,aliases=['Game']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def game (self,message):
        """ - Set Game"""
        if AdminCheck(message.message.author) == True:
            MessSplit = message.message.content
            AllVars = MessSplit.split(" ")
            Game = ""
            try:
                if AllVars[1] == "reset": #and not AllVars[2]:
                    yield from bot.change_presence(game=discord.Game(name='Totally Not Porn')) #Doesn't apply for some reason, until we do it twice...
                else:
                    for i in AllVars[1:]:
                        Game = Game+" "+i
                yield from bot.change_presence(game=discord.Game(name=Game))
            except IndexError:
                yield from self.bot.say("Please choose a game!")
        else:
            yield from self.bot.say("You think I'd let you change that? NOPE!")
        CommandRun(message.message.author,message.message.content)

    @commands.group(name="Stats",aliases=['stats'],pass_context=True, no_pm=False,invoke_without_command=True) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def stats(self,message):
        """- Stats for nerds"""
        yield from self.bot.say("Enter a subcommand for debugging stats")
        yield from self.bot.say("!help stats")
        CommandRun(message.message.author,message.message.content)
        
    @stats.command(name='Uptime',aliases=['uptime'], pass_context=True, no_pm=False)
    @asyncio.coroutine #Cuz Python 3.4
    def uptime(self, message):
        """ - How long have I been here?"""
        uptime = (datetime.datetime.now() - bot.uptime)
        fmt = '''H:MM:SS:NNNNNN\n*{0}*'''.format(uptime)
        yield from self.bot.say(fmt)
        CommandRun(message.message.author,message.message.content)

    @commands.command(name="Annoy",pass_context=True, no_pm=False,hidden=True)
    @asyncio.coroutine
    def annoy(self, message):
        try:
            process.poll
            print ("PILights Off")
            process.terminate()
            process.returncode()
            motephat.clear()
            motephat.show()
        except:
            print ("Not already Running, starting...")
            print ("PILights On")
            process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/rainbow.py"])
        yield from self.bot.say("So you found it...DAMN! Congrats {0}!".format(message.message.author.mention))
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False,hidden=True,enabled=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def addadmin(self,message):
        """- Y U SEE DIS?"""
        User = (str(message.message.author) + "\n")
        AdminFile = open(Admins,'a+')
        AdminFile.write(User)
        AdminFile.close
        CommandRun(message.message.author,message.message.content)

    @commands.group(name='VoiceChat',alias=['voicechat'],pass_context=True, invoke_without_command=True, no_pm=True)
    @asyncio.coroutine #Cuz Python 3.4
    def voicechat(self, message):
        """ - Voice Controls"""

    @voicechat.command(name="Join",pass_context=True, no_pm=True,aliases=['join'])
    @asyncio.coroutine #Cuz Python 3.4
    def join(self, message, *, channel : discord.Channel):
        """ - Joins a voice channel."""
        try:
            self.voice = yield from self.bot.join_voice_channel(channel)
            self.player = self.voice.create_ffmpeg_player('/home/pi/bin/Python/Memes/DTR.mp3')
            self.player.start()
        except discord.ClientException:
            yield from self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            yield from self.bot.say('This is not a voice channel...')
        else:
            yield from self.bot.say("Ready to play audio in {0}".format (channel.name))
            asyncio.sleep(5)
        CommandRun(message.message.author,message.message.content)

    @voicechat.command(name="Summon",pass_context=True, no_pm=True,aliases=['summon'])
    @asyncio.coroutine #Cuz Python 3.4
    def summon(self, message):
        """ - Summon to your Voice Channel"""
        print (message.message.author.voice_channel)
        try:
            voice_ch = message.message.author.voice_channel
            self.voice = yield from self.bot.join_voice_channel(voice_ch)
            yield from self.bot.say("Ready to play audio in {0}".format (voice_ch.name))
            #VoiceChannelsActive.append(voice_ch.name) #List of channels, in case stuck in a lot
            ##VoiceChannelsActive #debug, show list
        except discord.ClientException:
            yield from self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            yield from self.bot.say('You are not in a voice channel...')
        CommandRun(message.message.author,message.message.content)

    @voicechat.command(name="Leave",pass_context=True, no_pm=True,aliases=['leave'])
    @asyncio.coroutine #Cuz Python 3.4
    def leave(self, message, *, channel : discord.Channel):
        """ - Leaves a voice channel."""
        yield from self.voice.disconnect()
        #yield from client.voice.disconnect()
        print("Disconnecting voice")
        CommandRun(message.message.author,message.message.content)

    @voicechat.command(name="Play",pass_context=True, no_pm=True,aliases=['play'],enabled=True)
    @asyncio.coroutine #Cuz Python 3.4
    def play(self, message):
        self.player = self.voice.create_ffmpeg_player('/home/pi/bin/Python/Memes/Rich.mp3',use_avconv=True)
        self.player.start()
        while not self.player.is_done():
            yield from asyncio.sleep(1)
        yield from self.bot.voice.disconnect()

    @commands.group(pass_context=True, invoke_without_command=True, no_pm=True)
    @asyncio.coroutine #Cuz Python 3.4
    def test(self, message):
        print ("Test")
        print (dir(bot))
        #print (dir(message.message))
        print (bot.voice_client_in(message.message.server))
        
        
    @test.command(name='on', aliases=['enable', 'enabled'], pass_context=True, no_pm=True)
    @asyncio.coroutine #Cuz Python 3.4
    def test_on(self, message, *, channel: discord.Channel = None):
        """SubCommand"""
        print ("Test On")
        
    @test.command(name='off', aliases=['disable', 'disabled'], pass_context=True, no_pm=True)
    @asyncio.coroutine #Cuz Python 3.4
    def test_off(self, message):
        """SubCommand"""
        print ("Test Off")

class Memes: #Put all commands under here
    def __init__(self, bot):
        self.bot = bot #Give it 'passthrough', can't call bot if bot hasn't been defined until later
        #self.requester = message.author
        #self.channel = message.channel

    @commands.command(name="Triggered",pass_context=True, no_pm=False,aliases=['Trains','triggered']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def triggered(self,message):
        """- #TrainGate""" #This is the description as per the help command. bot.py must be edited to change how things are displayed.
        yield from self.bot.upload("/home/pi/bin/Python/Memes/Marine.png")
        #print (dir(message.message)) #View object attributes, useful for seeing where data sits
        CommandRun(message.message.author,message.message.content) #Pass function (command) name to function that logs

    @commands.command(name="Thanks",pass_context=True, no_pm=False,aliases=['thanks','budday','Budday','D3M0','d3m0','dmp30']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def thanks(self,message):
        """- Thanks Budday"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/DM.png")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="Richard",pass_context=True, no_pm=False, aliases=['MB']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def richard(self,message):
        """- ...In your kernels"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/Boniface.jpg")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="SMWYG",pass_context=True, no_pm=False, aliases=['Show Me What You Got','show me what you got']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def smwyg(self,message):
        """- ArmagHEADdon?!"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/SMWYG.gif")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="Sunday",pass_context=True, no_pm=False, aliases=['Ironing','ironing']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def sunday(self,message):
        """- Sunday blues"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/ironing.png")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="Aww",pass_context=True, no_pm=False, aliases=['Awh','awh']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def aww(self,message):
        """- Awh, Bitch!"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/AwB.gif")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name='GOMB',pass_context=True, no_pm=False, aliases=['gombb','GOMBB','Get off my back bitch','get off my back bitch','getoffmybackbitch','getoffmyback','get off my back','Get off my back']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def gomb(self,message):
        """- Get off my back"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/GOMBB.gif")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def inaflash(self,message):
        """- Barry Allen"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/ClarebooFlash.png")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False,hidden=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def broke(self,message):
        """- It was probably Jen..."""
        yield from self.bot.say("It's not a bug, it's a feature... back to the drawing board")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="LoR",pass_context=True, no_pm=False, aliases=['LOR','lor']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def LoR(self,message):
        """- LoR Assemble!"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/LoR.png")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="SD",pass_context=True, no_pm=False, aliases=['Service Desk','servicedesk','ServiceDesk','service desk','sd']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def SD(self,message):
        """- Pesky SD Memes"""
        Total = 2
        Meme = random.randint(1, Total)
        print (Meme)
        if Meme == 1:
            yield from self.bot.upload("/home/pi/bin/Python/Memes/OhNoHereCome.png")
        elif Meme == 2:
            yield from self.bot.upload("/home/pi/bin/Python/Memes/PeskySD.png")
        CommandRun(message.message.author,message.message.content)

    @commands.group(Name="Wintel",pass_context=True, no_pm=False, aliases=['wintel']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def Wintel(self,message):
        """- Damn Wintel"""
        if ("SmallText" in message.message.content or "smalltext" in message.message.content):
            pass
        else:
            Total = 3
            Meme = random.randint(1, Total)
            print (Meme)
            if Meme == 1:
                yield from self.bot.upload("/home/pi/bin/Python/Memes/Server.png")
            elif Meme == 2:
                yield from self.bot.upload("/home/pi/bin/Python/Memes/SponsorWintel.png")
            elif Meme == 3:
                yield from self.bot.upload("/home/pi/bin/Python/Memes/Hey_Man.png")
        CommandRun(message.message.author,message.message.content)
    
    @Wintel.command(name='SmallText',aliases=['smalltext'], pass_context=True, no_pm=False)
    @asyncio.coroutine #Cuz Python 3.4
    def smalltext(self, message):
        yield from self.bot.say("That is a secret...Shh!")

    @commands.command(Name="RIPJ",aliases=["ripj"], pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def rip(self,message):
        yield from self.bot.say("RIP Jives 02/02/2017 - 08/07/2017\nUnplugged too soon\nLong live Jives 2.0")
        CommandRun(message.message.author,message.message.content)

    @commands.command(Name="PTSDD",pass_context=True, no_pm=False, aliases=['ptsdd']) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def PTSDD(self,message):
        """- It's a scary place"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/PTSDD.png")
        CommandRun(message.message.author,message.message.content)

    @commands.group(name='Traincount',aliases=['traincount','Train Count','train count'],pass_context=True, invoke_without_command=True, no_pm=False)
    @asyncio.coroutine #Cuz Python 3.4
    def traincount(self,message):
        """ - How many has he missed?"""
        #print (dir(message.message)) #View object attributes, useful for seeing where data sits
        #MessSplit = message.message.content
        #AllVars = MessSplit.split(" ")
        #global TrainsMissed
        print (AdminCheck(message.message.author))
        try:
            TrainsMissed = GetSettings("TrainsMissed")
        except KeyError: #Cannot find Key in settings
            print ("Setting not found...")
        if TrainsMissed == 1:
            yield from self.bot.say("Gareth has missed {0} train *(Including 1 in 2008 or 2009)*".format(TrainsMissed))
        else:
            yield from self.bot.say("Gareth has missed {0} trains *(Including 1 in 2008 or 2009)*".format(TrainsMissed))
        CommandRun(message.message.author,message.message.content)

    @traincount.command(name='Add',aliases=['add'],pass_context=True, no_pm=False,hidden=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def traincount_Add(self, message, *, channel: discord.Channel = None): #Need a way to implement this perm
        if AdminCheck(message.message.author) == True:
            TrainsMissed = TrainsMissed + 1
            if TrainsMissed == 1:
                yield from self.bot.say("Gareth has missed {0} train *(Including 1 in 2008 or 2009)*".format(TrainsMissed))
            else:
                yield from self.bot.say("Gareth has missed {0} trains *(Including 1 in 2008 or 2009)*".format(TrainsMissed))
        else:
            yield from self.bot.say("You think I'd let you change that? NOPE!")
        CommandRun(message.message.author,message.message.content)

    @traincount.command(name='Remove',aliases=['remove'],pass_context=True, no_pm=False,hidden=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def traincount_Remove(self, message, *, channel: discord.Channel = None): #Need a way to implement this perm
        if AdminCheck(message.message.author) == True:
            TrainsMissed = TrainsMissed - 1
            if TrainsMissed == 1:
                yield from self.bot.say("Gareth has missed {0} train *(Including 1 in 2008 or 2009)*".format(TrainsMissed))
            else:
                yield from self.bot.say("Gareth has missed {0} trains *(Including 1 in 2008 or 2009)*".format(TrainsMissed))
        else:
            yield from self.bot.say("You think I'd let you change that? NOPE!")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def maybe(self,message):
        """- *Maybe*"""
        yield from self.bot.say("*maybe* - Clareboo, Whitelist King")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def sick(self,message):
        """- >>"""
        yield from self.bot.say("It's all fun and games until somebody breaks out the sick aerials!")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def late(self,message):
        """- Oh no"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/Class.gif")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def hello(self,message):
        """- I say hello"""
        yield from self.bot.say("Hello, {0}!".format(message.message.author.mention))
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def crazytrain(self,message):
        """ - Crazy Trains"""
        fmt = """*He's going off the rails 'cause he missed the train!*\n    - In the style of Ozzy Osbourne (Crazy Train)"""
        yield from self.bot.say(fmt)
        yield from self.bot.upload("/home/pi/bin/Python/Memes/MissedTheTrain.png")
        CommandRun(message.message.author,message.message.content)

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def patchit(self,message):
        """- Just to be sure"""
        yield from self.bot.upload("/home/pi/bin/Python/Memes/BeltAndBraces.png")
        CommandRun(message.message.author,message.message.content)      

    @commands.command(pass_context=True, no_pm=False) #Passthrough, and showing it's a command
    @asyncio.coroutine #Cuz Python 3.4
    def singmeasong(self,message):
        """- Sing me a song"""
        TotalQuotes = 5
        Quote = random.randint(1, TotalQuotes)
        print (Quote)
        if Quote == 1:
            fmt = """\n*Well, who are you? (Clareboo? who, who, who, who?)*\n    - In the style of The Who (Who Are You)"""
            yield from self.bot.say(fmt)
        elif Quote == 2:
            fmt = """\n*Clareboo\nClareboo\nClareboo Nah Nah*\n    - In the style of Fat Les (Vindaloo)"""
            yield from self.bot.say(fmt)
        elif Quote == 3:
            fmt = """\n"Clareboo, Clareboo, ooh ooh"\n    - In the style of Taylor Swift (Shake It Off)"""
            yield from self.bot.say(fmt)
        elif Quote == 4:
            fmt = """\n*Clareeeeboo, Clareeeeboo,\nTake my hand\nWe're off to never never land*\n    - In the style of Metallica (Enter Sandman)"""
            yield from self.bot.say(fmt)
        elif Quote == 4:
            fmt = """\n*Clareeeeboo!, Burning out his fuse up here alone*\n    - In the style of Elton John (Rocket Man)"""
            yield from self.bot.say(fmt)
        elif Quote == 5:
            fmt = """\n*So you'll know that\nI'm ClarebooOoo, I'm ClarebooOoo, I'm Clareboo*\n    - In the style of Union J (Carry You)"""
            yield from self.bot.say(fmt)
        CommandRun(message.message.author,message.message.content)


print ("Starting Server...")
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Bot Bois Bitch Basic (B)instructions") #Commands are ![Command] or @[Botname] [Command]
bot.add_cog(Commands(bot)) #This is how it accesses the class, see below.
bot.add_cog(Memes(bot)) #This is how it accesses the class, see below.
"""A cog is a class that has its own event listeners and commands.
   They are meant as a way to organize multiple relevant commands
   into a singular class that shares some state or no state at all."""

@bot.event
@asyncio.coroutine #Cuz Python 3.4
def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        yield from bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        yield from bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_member_join(member):
    yield from bot.say("Welcome to the scrubs {}!".format(member))

@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_member_remove(member):
    yield from bot.say("{0} Got kicked from the promised land!".format(member))

@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_server_emojis_update(before,after):
    print ("Was: \n",before)
    print ("Now: \n",after)
    discord_logger.info("[{0}] >Emojis Updated".format(datetime.datetime.now()))

@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_server_unavailable (server):
    print ("{} Now unavailable".format(server))
    discord_logger.info("[{0}] >Server '{1}' unavailable".format(datetime.datetime.now(),server))
   
@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_voice_state_update (before, after): #Must already be in the chat!!!
    print (dir(after))
    if after.voice_channel is not before.voice_channel: #This will only trigger if they move / join channel
        #print ("Somebody moved Voice Channel")
        print (bot.is_voice_connected(after.server))
        if after.voice_channel is not None:
            print (after.name,"joined",after.voice_channel)
            if after.name == "richofthehour":
                pass
            elif after.name == "That Babylonian Bum":
                pass
            elif after.name == "ArsoN":
                pass
            elif after.name == "James":
                pass                
            elif after.name == "Gazzllan":
                pass
            elif after.name == "GWYN554":
                pass                
            elif after.name == "andonisgun":
                pass                
            elif after.name == "Stevealou":
                pass                
            elif after.name == "Tagnote":
                pass                
        else:
            print (after.name,"left",before.voice_channel)

''' Leave commented out while testing
@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_server_join(server):
    fmt = """
Look who just joined your channel... Here come that, {}
o shit waddup"""
    yield from bot.send_message(server.default_channel,fmt.format(bot.user.name))
'''

@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_socket_opened():
    print("Socket Open, Almost ready")

@bot.event #For each event, need one of these also
@asyncio.coroutine #Cuz Python 3.4
def on_ready():
    users = len(set(bot.get_all_members()))
    server = len(bot.servers)
    channels = len([c for c in bot.get_all_channels()])
    yield from bot.change_presence(game=discord.Game(name='Totally Not Porn'))
    print("------")
    print("{} is now online.".format(bot.user.name))
    print("API Version: ",discord.__version__)
    print("ID: ",bot.user.id)
    print("Connected to:")
    print("{} servers".format(server))
    print("{} channels".format(channels))
    print("{} users".format(users))
    print("Bot URL: https://discordapp.com/oauth2/authorize?&client_id="+bot.user.id+"&scope=bot&permissions=0")
    print ("Voice Enabled: {}".format(discord.opus.is_loaded()))
    print ("Log File: '{}'".format(logging.getLoggerClass().root.handlers[0].baseFilename))
    print("------")
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()
    fmt = '[{0}] Bot started'.format(datetime.datetime.now())
    discord_logger.info(fmt)
    #print (dir(bot))

Key = sys.argv[1]
bot.run(Key)

handlers = log.handlers[:]
for hdlr in handlers:
    hdlr.close()
log.removeHandler(hdlr)