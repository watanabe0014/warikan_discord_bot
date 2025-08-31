import json
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import payments
import users

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(os.getenv("DISCORD_TOKEN")) 
payments.init_db()

intents = discord.Intents.default()
intents.message_content = True  # Message Content Intent をONにした場合
bot = commands.Bot(command_prefix="!", intents=intents)

payments = {}  # {user_id: amount}


### 2025/09/01 guild_idをuser_idで代用するように修正予定

@bot.command()
async def test(ctx):
    print(ctx.author.id)

@bot.command()
async def pay(ctx, amount: int, reason=""):
    payments.add_payment(str(ctx.guild.id), str(ctx.author.id), amount, reason)
    await ctx.send(f"{ctx.author.mention} が {amount}円 を支払いました（{reason}）")

@bot.command()
async def warikan(ctx):
    if not payments:
        await ctx.send("記録がありません。")
        return
    
    total = sum(payments.values())
    members = len(payments)
    average = total // members
    
    balances = {uid: amt - average for uid, amt in payments.items()}
    
    # プラス組・マイナス組に分ける
    creditors = [(uid, bal) for uid, bal in balances.items() if bal > 0]
    debtors   = [(uid, -bal) for uid, bal in balances.items() if bal < 0]
    
    creditors.sort(key=lambda x: -x[1])  # 多く払った順
    debtors.sort(key=lambda x: -x[1])    # 多く借りた順
    
    result = []
    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor_id, credit = creditors[i]
        debtor_id, debt = debtors[j]
        
        transfer = min(credit, debt)
        
        creditor = await bot.fetch_user(creditor_id)
        debtor   = await bot.fetch_user(debtor_id)
        result.append(f"{debtor.display_name} → {creditor.display_name} に {transfer}円 支払う")
        
        creditors[i] = (creditor_id, credit - transfer)
        debtors[j]   = (debtor_id, debt - transfer)
        
        if creditors[i][1] == 0:
            i += 1
        if debtors[j][1] == 0:
            j += 1
    
    await ctx.send("割り勘結果:\n" + "\n".join(result))

@bot.command()
async def reset(ctx):
    payments.clear()
    await ctx.send("支払い記録をリセットしました。")

bot.run(TOKEN)
