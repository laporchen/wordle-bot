import discord
import json
from discord import client
from discord.ext import commands
import libWordle as wd
keyPath = "./key.json"

# wordle variables
wordleGameStarted = {}
wordList = []
puzzle = {}
guessCount = {}
guessResult = {}
# end wordle

client = commands.Bot(command_prefix='!')


def getKey(path):
    with open(path, 'rb') as f:
        data = json.load(f)
        return data['Key']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command(pass_context=True, aliases=['wd'])
async def wordle(ctx, arg="2"):
    serverId = str(ctx.guild.id)
    global wordleGameStarted, puzzle, wordList, guessCount, guessResult
    if(serverId not in wordleGameStarted):
        wordleGameStarted[serverId] = False
        puzzle[serverId] = ""
        guessCount[serverId] = 0
        guessResult[serverId] = []
    if(arg == "help"):
        await ctx.send(ctx.author.mention + " 可以用的指令有：\n" + "$wordle new 開始遊戲\n" + "$wd word 猜字\n")
    if(arg == "new" and wordleGameStarted[serverId] == False):
        wordleGameStarted[serverId] = True
        wordList = wd.init()
        puzzle[serverId] = wd.gameInit(wordList['words'])
        guessCount[serverId] = 0
        await ctx.send("遊戲開始，輸入$wordle <word> 來進行猜測")
    elif(arg == "new" and wordleGameStarted[serverId] == True):
        await ctx.send("遊戲已經開始了，使用$wordle <word> 來猜")
    elif (wordleGameStarted[serverId]):
        res = wd.process(
            arg, puzzle[serverId], wordList['words'], wordList['allowGuesses'])
        if(res[2] == False):
            await ctx.send(ctx.author.mention + res[1])
            return
        guessResult[serverId].append(res[1])
        guessCount[serverId] += 1
        if(res[0] == True):
            await ctx.send(res[1])
            await ctx.send("遊戲結束，猜測次數: " + str(guessCount[serverId]))
            guessStr = ""
            for i in guessResult[serverId]:
                guessStr += i + "\n"
            await ctx.send(guessStr)
            wordleGameStarted[serverId] = False
            return
        await ctx.send(res[1])
        if(guessCount[serverId] > 5):
            await ctx.send("遊戲結束，輸入$wordle new 重新開始\n" + "答案是：" + puzzle[serverId])
            wordleGameStarted[serverId] = False
            return

intents = discord.Intents().all()
key = getKey(keyPath)
client.run(key)
