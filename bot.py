import os
import discord
from discord.ext import commands

# إعدادات البوت والصلاحيات
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# الآيدي الخاص بالروم الصوتي اللي بيدخل له البوت
VOICE_CHANNEL_ID = 1344916160751206446  # آيدي الروم الصوتي حقك

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")
    
    # محاولة الدخول للروم الصوتي تلقائياً فور تشغيل البوت
    try:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f"تم بنجاح الانضمام إلى الروم الصوتي: {channel.name}")
        else:
            print("لم يتم العثور على الروم الصوتي أو أن الآيدي غير صحيح!")
    except Exception as e:
        print(f"حدث خطأ أثناء محاولة الاتصال الصوتي: {e}")

@bot.command()
async def join(ctx):
    """أمر يدوي لدخول الروم إذا خرج البوت"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"تم الدخول إلى روم: **{channel.name}** بنجاح!")
    else:
        await ctx.send("يجب أن تكون في روم صوتي أولاً لكي أتمكن من الدخول معك!")

@bot.command()
async def leave(ctx):
    """أمر لإخراج البوت من الروم الصوتي"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم الخروج من الروم الصوتي.")
    else:
        await ctx.send("أنا لست في أي روم صوتي أساساً!")

# تشغيل البوت باستخدام متغير البيئة الآمن من الاستضافة
bot.run(os.getenv("DISCORD_TOKEN"))
