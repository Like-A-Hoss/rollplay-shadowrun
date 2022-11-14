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




@client.slash_command(name="info", description="Get instruction from the Roll Play on how to use for Exalted.")
async def infoc(interaction:Interaction):
    await interaction.response.send_message("Hello Nobel One!  I am Roll Play for Exalted!\n I will be able to roll dice and do dice tricks.\n   For now just basic roll, and join battle are working, the other rolls are under redevelopment, I cannot gaurentee their functionality.  I should have them back up soon, reworked to a new logic.\n  Build 48")

@client.slash_command(name="basicroll", description="Basic roll. No dice tricks.")
async def basic_roll(interaction:Interaction, dicepool:int, difficulty:int = 1, willpower:bool =False, excelency:int =0, stunt:bool =True, double:int =10):
    print("new attempt")
    roller = dice.Exalted_Dice(dicepool, willpower, excelency, stunt)    
    results = roller.basic_roll()
    sux = roller.count_successes(results, double)
    message_maker = Message_Maker()
    #let's get those bonuses, to display in our output embed
    bonuses = "You recieved the following bonuses:\n"
    if willpower:
        bonuses += "\nwith 1 bonus success from Willpower"
    if stunt == True:
        bonuses += "\n2 extra dice from a stunt"
    if excelency >0:
        bonuses += f"\n and {excelency} extra dice from an excellency"
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

@client.slash_command(name="join_battle", description="The Battle Starts")
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

@client.slash_command(name="withering_attack", description="Basic roll, no dice tricks yet, corrected error in subtracting defense from dice pool.")
async def witheringA(interaction:Interaction, dice_pool:int, defence:int, willpower:bool =False, excelency:int=0, stunt:bool=True, double:int=10):
    print("new attempt")
    roller = dice.Exalted_Dice(dice_pool, willpower, excelency, stunt)    
    message_maker = Message_Maker()
    results = roller.basic_roll()
    sux = roller.count_successes(results, double)
    bonuses = "You recieved the following bonuses:\n"
    if willpower:
        bonuses += "\nwith 1 bonus success from Willpower"
    if stunt == True:
        bonuses += "\n2 extra dice from a stunt"
    if excelency >0:
        bonuses += f"\n and {excelency} extra dice from an excellency"
    
    if sux >= 1 and sux >= defence:
        success = "success"
        message = message_maker.attack(interaction, results, sux, success, bonuses, defence)
    else:
        botch = roller.check_botch(results=results)
        if botch == True:
            success = "botch"
            message = message_maker.attack(interaction, results, sux, success, bonuses, defence)# Byte-compiled / optimized / DLL files
        else:
            success = "failure"
            message = message_maker.attack(interaction, results, sux, success, bonuses, defence)
    await interaction.response.send_message(embed=message)

@client.slash_command(name="decisive_attack", description="Basic roll will ask for Attribute and Ability, no rerolls are factored in yet")
async def decisiveA(interaction:Interaction, dice_pool:int, defence:int, willpower:bool =False, excelency:int =0, stunt:int=1, double:int =10):
    print("new attempt")
    roller = dice.Exalted_Dice(dice_pool, willpower, excelency, stunt)    
    results = roller.basic_roll()
    sux = roller.count_successes(results, double)
    message_maker = Message_Maker()
    bonuses = "You recieved the following bonuses:\n"
    if willpower:
        bonuses += "\nwith 1 bonus success from Willpower"
    if stunt >= 1:
        bonuses += "\n2 extra dice from a stunt"
    if stunt >= 2:
        bonuses += "\na bonus success from a great stunt!"
    if excelency >0:
        bonuses += f"\n and {excelency} extra dice from an excellency"
    if sux >= 1 and sux >= defence:
        success = "success"
        message = message_maker.attack(interaction, results, sux, success, bonuses, defence)
    else:
        botch = roller.check_botch(results=results)
        if botch == True:
            success = "botch"
            message = message_maker.attack(interaction, results, sux, success, bonuses, defence)
        else:
            success = "failure"
            message = message_maker.attack(interaction, results, sux, success, bonuses, defence)
    await interaction.response.send_message(embed=message)

@client.slash_command(name="withering_dmg", description="Generates Withering Damage", guild_ids=[testingServerID])
async def withering_damage(interaction:Interaction, extra_successes:int, damage:int, strength:int, soak:int, excelence:int =0, bonus:int = 0, double:int = 10):
    soak = soak
    enemy_initative = enemy_initative
    pool = extra_successes + damage + strength + bonus
    roller = dice.Exalted_Dice(pool, willpower=False, excelence=excelence, stunt=False)
    raw_damage = pool  
    results = roller.roll_withering_damage(raw_damage, soak)
    sux = roller.count_successes(results, double)
    message_maker = Message_Maker()
    initative_gained = 0
    if sux >= 1:
        initative_gained += sux +1
        message = message_maker.withering_damage_msg(interaction, results, sux, soak, initative_gained)
        if sux >= enemy_initative:
            enemy_initative -= sux
            initative_gained += 5
            message = message_maker.withering_damage_msg(interaction, results, sux, soak, initative_gained)
    else:
        initative_gained += 1
        message = message_maker.withering_damage_msg(interaction, results, sux, soak, enemy_initative, initative_gained)
    #message = message_maker.withering_damage_msg(interaction, results, sux, soak, enemy_initative, initative_gained)
    await interaction.response.send_message(embed=message)

@client.slash_command(name="add_character", description="adds character to game", guild_ids=[testingServerID])
async def add_character(interaction:Interaction, id:int,nick_name:str):
    connection = lot_casting_model.Lot_Casting_Atemi.api_connect("character", id)
    character = Character(connection['name', nick_name, connection['']])

@client.slash_command(name="test", description="API test", guild_ids=[testingServerID])
async def testing(interaction:Interaction):
    #await interaction.response.send_message("Starting test")
    testing_elemental = lot_casting_model.Lot_Casting_Atemi()
    test_data = testing_elemental.test_api()
    #response_API = requests.get('https://www.lotcastingatemi.com/api/v1/characters/19964')
        #print(response_API.status_code)
    #data = response_API.text
    #await interaction.response.send_message("data retreived")
    #parsed_data = json.loads(data)
    #test_data = parsed_data['name']
    await interaction.response.send_message(test_data)

@client.slash_command(name="test_roller_stunt", description="test roller for stunt failure",  guild_ids=[testingServerID])
async def test2(interaction:Interaction, dice_pool =5, willpower =False, excelency =0, stunt =False):
    roller = dice.Exalted_Dice(dice_pool, willpower, excelency, stunt)
    check= roller.get_stunt()
    check2 = roller.basic_roll()
    check3 = roller.count_successes(check2, 10)

    bonuses = "so far no..."
    if willpower:
        bonuses += "\nwith 1 bonus success from Willpower"
    if stunt:
        bonuses += "\n2 extra dice from a stunt"
    if excelency >0:
        bonuses += f"\n and {excelency} extra dice from an excellency"

    await interaction.response.send_message(f"Stunt is set to {check}, results: {check2}, counted {check3}, is it in bonus? {bonuses}")

@client.slash_command(name="test_reroll_6", description="test roller to see if reroll all works", guild_ids=[testingServerID])
async def test3(interaction:Interaction, dice_pool = 30, willpower = False, excelency = 0, stunt = False):
    roller = dice.Exalted_Dice(dice_pool, willpower, excelency, stunt)
    results = roller.basic_roll()
    rerolls = roller.check_reroll_all(results, 6)
    
    await interaction.response.send_message(f" the innitail roll was {results}, the reroll was{rerolls}")

client.run(SECRET_KEY)