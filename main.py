import os
import discord
from discord.ext import commands
import random
import re
from myserver import server_on

# ต้องเปิด message_content intent ใน Discord Developer Portal ด้วย!
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="r", intents=intents)

def roll_custom_d6():
    roll = random.randint(1, 6)
    if roll == 1:
        score = -1
        desc = "1 ❌ Critical Fail (-1)"
    elif roll in [2, 4]:
        score = 1
        desc = f"{roll} ➕ (+1)"
    elif roll == 6:
        score = 2
        desc = "6 🌟 Critical (+2)"
    else:  # 3, 5
        score = 0
        desc = f"{roll} (0)"
    return roll, score, desc

def roll_d2():
    roll = random.randint(1, 2)
    return "หัว" if roll == 1 else "ก้อย"

@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมทำงานแล้ว!")

@bot.command(name="r")
async def roll(ctx, *, arg):
    # รองรับทั้ง + และ - เช่น 3d6 +2 หรือ 3d6 -2
    match = re.match(r"(\d+)d(\d+)(?:\s*([+-]\d+))?", arg.strip())
    if not match:
        await ctx.send("❌ รูปแบบไม่ถูกต้อง! ใช้แบบนี้: r3d6 +2 หรือ r3d6 -1")
        return

    num_dice = int(match.group(1))
    dice_type = int(match.group(2))
    bonus = int(match.group(3)) if match.group(3) else 0

    results = []
    total_score = 0

    if dice_type == 6:  # custom d6
        for _ in range(num_dice):
            roll, score, desc = roll_custom_d6()
            results.append(desc)
            total_score += score
        total_score += bonus
        result_text = "\n".join(results)
        sign = f"+{bonus}" if bonus >= 0 else f"{bonus}"
        await ctx.reply(
            f"{ctx.author.mention} 🎲 ทอย {num_dice}d6 {sign}\n{result_text}\nรวมแต้ม: **{total_score}**"
        )

    elif dice_type == 2:  # d2 เหรียญ
        for _ in range(num_dice):
            results.append(roll_d2())
        result_text = ", ".join(results)
        await ctx.reply(f"{ctx.author.mention} 🪙 ทอย {num_dice}d2\nผลลัพธ์: {result_text}")

    else:
        await ctx.reply("❌ ตอนนี้รองรับแค่ d6 (custom) และ d2 เท่านั้น!")

server_on()

bot.run(os.getenv('TOKEN'))

