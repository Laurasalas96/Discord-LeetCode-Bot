
from random import randrange
from datetime import date
from datetime import datetime
import discord, re, warnings 
from discord.ext import tasks
from discord.ext import commands


################CONFIG THIS TO YOUR DISCORD SERVER ################
BOT_DESCRIPTION = "A bot that gives random leetcodes"
description = BOT_DESCRIPTION

#TOKEN OF BOT 
TOKEN = 'Your bot token here'

#CHANNEL IDs
#This is the channel where the bot will send the leetcode requests from users
#that request a problem from it
#commented out so users can request leetcode from any channel, otherwise uncomment this. 
#CHANNEL_ID_TO_REQUEST_LC = 00000000000

#This is the channel where the bot will send a daily easy,medium and hard discord.
CHANNEL_ID_TO_SEND_DAILY_LC = 111111111

#Paths (relative) of where the problems are stored. If you want to add a leetcode problem,
#go in the respective difficulty text file. 
PATHS=["easy.txt", "medium.txt", "hard.txt"]


##################################################################

# Leetcode problems
easy = []
medium = []
hard = []

# Link generating methods 

def importLeetcodes(easyPath, mediumPath, hardPath):
    """
    Imports the leetcode problem urls from the text files.
    Each text file must have one valide leetcode url per line
    otherwise it will return an error.
    """
    pattern = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
    p = re.compile(pattern, re.IGNORECASE)

    def checkIfValidURLs(currURL):
        return p.match(currURL)

    for filePath in easyPath,mediumPath,hardPath:
        file = open(filePath, "r")
        lineCount = 1
        for x in file:
            line = str(x)
            line = line.replace("\n", "")
            if not checkIfValidURLs(line):
                warnings.warn("\nProblem with a URL on line " + str(lineCount) + " of file " + filePath + "\n" + \
            "Please make sure each line in the file has a valid url, with no other characters before or after it.")
                return
            if filePath is easyPath:
                easy.append(line)
            elif filePath is mediumPath:
                medium.append(line)
            else:
                hard.append(line)
            lineCount += 1
    print("Leetcode problems from files imported succesfully!")



importLeetcodes(PATHS[0], PATHS[1], PATHS[2])

def updateDBIfneeded():
	"""
	in case something weird happens where the import is not saved on memory anymore
	"""
	if not easy or not medium or not hard: 
		importLeetcodes(PATHS[0], PATHS[1], PATHS[2])




def giveDailyProblem():
    """
    Composes daily messages to send, from the list above.
    :return:
    """
    #
    greetings = [
        "Heeeelllooo! ",
        "Gooood mornin' ",
        "*dabs* ",
        "Howdy, ",
        "*zzZzzZ*...........",
        "Beep. boop. ",
        "Hi everyone! ",
        "psst! "
    ]

    # Chooses the message randomly from the lists above, never giving the same problem twice
    # Note, however, that once it goes over the 50 leetcodes of each difficulty,
    # it will start to repeat itself.
    date_format = "%m/%d/%Y"
    a = datetime.strptime('1/25/2021', date_format)
    b = datetime.today()
    delta = b - a
    dayNumber = delta.days

    greetingNo = randrange(len(greetings))

	updateDBIfneeded()
	
    easyUrl = easy[dayNumber % len(easy)]
    mediumUrl = medium[dayNumber % len(medium)]
    hardUrl = hard[dayNumber % len(hard)]

    daily = "here are today's daily leetcodes #%d : \n \
    LC easy for those that want to take it easy: %s \n \
    LC medium for those who don't have time to waste: %s \n \
    LC hard for the beasts: %s" % (
    dayNumber + 1, easyUrl, mediumUrl, hardUrl)

    return greetings[greetingNo] + daily



def giveRandomProblem(difficulty):
    """
    Gives a leetcode url according to given difficulty indicated by user
    :param difficulty: random, easy, medium or hard.
    :return: the generated problem string
    """
	updateDBIfneeded()
	
    if difficulty == "easy":
        problemNo = randrange(len(easy))
        return "A lil' easy-peasy problem: " + easy[problemNo]
    elif difficulty == "medium":
        problemNo = randrange(len(medium))
        return "You get a medium problem! " + medium[problemNo]
    elif difficulty == "hard":
        problemNo = randrange(len(hard))
        return "Oof, here is a hard one. Good luck! " + hard[problemNo]
    elif difficulty == "surprise":
        diff = randrange(0, 3)
        print(diff)
        problem = ""
        if diff == 0:
            problemNo = randrange(len(easy))
            problem = easy[problemNo]
        elif diff == 1:
            problemNo = randrange(len(medium))
            problem = medium[problemNo]
        elif diff == 2:
            problemNo = randrange(len(hard))
            problem = hard[problemNo]
        return "You have requested an unknown difficulty problem... Here it is." + problem


# DISCORD METHODS 
client = discord.Client()
bot = commands.Bot(command_prefix='?', description=description)


@tasks.loop(minutes=1)
async def sendDaily():
    """
    Gives a set of an easy, a medium and a hard leetcode once per day.
    """
    channel = client.get_channel(CHANNEL_ID_TO_SEND_DAILY_LC)

    # Makes sure that the daily leetcode was not already sent that day, just in case the server
    # is restarted or something
    async for mussage in channel.history(limit=200):
        if mussage.author == client.user and mussage.created_at.strftime("%d/%m/%y") == \
                datetime.today().strftime("%d/%m/%y"):
            return

    await channel.send(giveDailyProblem())


@bot.command()
async def random_problem(ctx, difficulty: str):
    """
    Gives a random problem to the user
    :param difficulty: could be easy, medium, hard or random
    :return: the chosen leetcode, as a message on the server
    """
    await ctx.send(giveRandomProblem(difficulty))


@client.event
async def on_ready():
    # for console usage, to know that your server is working
    sendDaily.start()
    print('We have logged in as {0.user}'.format(client))


# Receive command to give out a random problem 
@client.event
async def on_message(message):
    """
    Allows the user to interact with the bot: ask for a random problem, or ask for the
    commands
    :param message: must start with '$yeet'
    :return: the message to the
    """
    help = "How to request a leetcode: \n \
     `$yeet random_problem easy` gives a leetcode easy \n \
      `$yeet random_problem medium` gives a medium \n \
      `$yeet random_problem hard` gives a hard \n \
      `$yeet random_problem surprise` gives a leetcode \
       with unknown difficulty (easy or medium or hard) "

    #uncomment this line if you want to restrict where the user requests the problems
    # if not message.channel == CHANNEL_ID_TO_REQUEST_LC:
    #     return

    channel = message.channel

    if message.author == client.user:
        return
    if message.content.startswith("$yeet random_problem easy"):
        await channel.send(giveRandomProblem("easy"))
    elif message.content.startswith("$yeet random_problem medium"):
        await channel.send(giveRandomProblem("medium"))
    elif message.content.startswith("$yeet random_problem hard"):
        await channel.send(giveRandomProblem("hard"))
    elif message.content.startswith("$yeet random_problem surprise"):
        await channel.send(giveRandomProblem("surprise"))
    elif message.content.startswith("$yeet help"):
        await channel.send(help)
    #todo: maybe add a message to handle when the bot doesn't understand what is being said?


client.run(TOKEN)