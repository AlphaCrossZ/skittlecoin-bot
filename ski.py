import discord
from discord.ext import commands
import os
import json
import random
import time
from webserver import keep_alive
#these are all of the modules that I have imported.

percentage_chance = 0.5
#added this for a ddajki feature, removed it. I just wanted to check how it worked.

client = commands.Bot(command_prefix="ski!")
#ski! is the command prefix for the skittlecoin bot. This is used before calling an action so the bot can respond.




@client.event
async def on_ready():
    #on_ready is used as 
    await client.change_presence(activity=discord.Game(name="ski!help"))
    #This gives the bot a status like it's playing a game. The game is "ski!help". This is the command to see all of the bot's commands.
    print('We have logged in as {0.user}'.format(client))
    #This shows that the code has successfully connected to the bot profile.

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("economy.json", "w") as f:
        json.dump(users, f, indent=4)
    return True


async def get_bank_data():
    with open("economy.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("economy.json", "w") as f:
        json.dump(users, f, indent=4)

    bal = [users[str(user.id)]["wallet"]], users[str(user.id)["bank"]]
    return bal


@client.command(aliases=["bal"])
async def balance(ctx, user: discord.Member = None):
    if not user:
        user = ctx.author
    await open_account(user)

    users = await get_bank_data()
    user = user

    wallet_amount = users[str(user.id)]["wallet"]
    bank_amount = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{user}'s swag balance", color=000000)
    embed.add_field(name="Wallet", value=f"{wallet_amount}")
    embed.add_field(name="Bank", value=f"{bank_amount}")

    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): #checks if on cooldown
        msg = "slow down, buckaroo, you have {:.2f}s left".format(error.retry_after) #says the time
        await ctx.send(msg) #send the error message
        #note: {:.2f} is too shorten the decimals. Example: 3.128343 would be 3.12

@client.command(aliases=["m"])
@commands.cooldown(2,21600,commands.BucketType.user)
async def mine(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(
        f"You used the power of the funny and mined {earnings} skittlecoin!!")

    users[str(user.id)]["wallet"] += earnings

    with open("economy.json", "w") as f:
        json.dump(users, f, indent=4)

async def update_bank(user, change = 0, mode = "wallet"):
  users = await get_bank_data()

  users[str(user.id)][mode] += change
  
  with open("economy.json","w") as  f:
    json.dump(users,f,indent=4)
  
  bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
  return bal

@client.command(aliases=["w"])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("you need to withdraw a number, dummy")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("you're not elon (funnyman) musk, you don't have that much funny money")
        return
    if int(amount) < 0:
        await ctx.send("ok, so here me out, you can't withdraw a negative number")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "bank")

    await ctx.send(f"you withdrew {amount} SKI!!")

async def update_bank(user, change = 0, mode = "wallet"):
  users = await get_bank_data()

  users[str(user.id)][mode] += change
  
  with open("economy.json","w") as  f:
    json.dump(users,f,indent=4)
  
  bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
  return bal

@client.command(aliases=["d"])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("you need to deposit a number, dummy")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("you're not elon (funnyman) musk, you don't have that much funny money")
        return
    if int(amount) < 0:
        await ctx.send("ok, so here me out, you can't deposit a negative number")
        return

    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"you deposited {amount} SKI!!")

@client.command(aliases=["p"])
async def pay(ctx,member:discord.Member,amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
         await ctx.send("you need to pay your client a real number, dummy")
         return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("you're not elon (funnyman) musk, you don't have that much funny money")
        return
    if int(amount) < 0:
        await ctx.send("ok, so here me out, you can't deposit a negative number")
        return

    await update_bank(ctx.author, -1 * amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"you payed {member} {amount} SKI!!")



keep_alive()
client.run("put your token here!")
