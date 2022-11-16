from hashlib import new
from sqlite3 import connect
import nextcord
#import random
from nextcord.ext import commands
from nextcord import Embed, Interaction
from embed_message_maker import Message_Maker
from setting import SECRET_KEY as SECRET_KEY
from setting import testingServerID as testingServerID
import dice

#import json
#import requests


init_list = []

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix ='!', intents=intents)



@client.event
async def on_ready():
    print("Hello Papa!\n")




@client.slash_command(name="info", description="Get instruction from the Roll Play on how to use for Shadowrun.")
async def infoc(interaction:Interaction):
    await interaction.response.send_message("Hello Chummer!  I am Roll Play for Shadowrun!\n I will be able to roll dice trackinitative.\n   For now just basic rolls and rolls with pre-edge are working.\n  I should have Iniatives up soon.\n  Rolls can be done with /roll  Build 01")

@client.slash_command(name="roll", description="Basic roll. with our without edge.")
async def basic_roll(interaction:Interaction, dicepool:int, difficulty:int = 1, edge:bool =False):
    print("new attempt")
    roller = dice.Shadowrun5_Dice(dicepool, edge)    
    results = roller.basic_roll()
    sux = roller.count_hits(results)
    message_maker = Message_Maker()
    #let's get those bonuses, to display in our output embed
    bonuses = "You recieved the following bonuses:\n"
    if edge:
        bonuses += "\nYou used a point of edge to add extra dice and gain exploding 6's."
    
    #Now lets get our dice set up    
    #Now lets see which embed we need
    if sux > 0 and sux >= difficulty:
        message = message_maker.sucess(interaction, results, sux, bonuses, difficulty)
    elif sux > 0 and sux < difficulty:
        #await interaction.response.send_message(f"THis is a failed roll, {results} generating Embed")
        message = message_maker.fail(interaction=interaction, results=results, bonuses=bonuses, sux=sux, difficulty=difficulty)
    else:
    #    await interaction.response.send_message("This is a botch")
        message = message_maker.botch(interaction=interaction, results=results, sux=sux, bonuses=bonuses, difficulty=difficulty)
    await interaction.response.send_message(embed= message)

@client.slash_command(name="SR5 Initative", description="The Battle Starts")
async def jb_roll(interaction:Interaction, dice_pool:int, willpower:bool =False, excelency:int =0, stunt:bool =True, double:int =10, dawn:bool=False):
    print("new Initative")
    roller = dice.Exalted_Dice(dice_pool, willpower, excelency, stunt)    
    results = roller.basic_roll()
    sux = roller.count_successes(results, double)
    message_maker = Message_Maker()
    if not dawn:
        initative =sux + 3
    else:
        initative = sux + 5
    #let's get those bonuses, to display in our output embed
    bonuses = "You recieved the following bonuses:\n"
    if willpower:
        bonuses += "\nwith 1 bonus success from Willpower"
    if stunt == True:
        bonuses += "\n2 extra dice from a stunt"
    if excelency >0:
        bonuses += f"\n and {excelency} extra dice from an excellency"

    message = message_maker.initative(interaction, results, bonuses, initative)
    await interaction.response.send_message(embed=message)


client.run(SECRET_KEY)