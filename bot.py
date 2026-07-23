import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

VOICE_CHANNEL_ID = 1234567890123456789

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")
    
    # محاولة الدخول المباشر أول ماشتغل البوت
    try:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel:
            # إذا كان متصل بروم قديم بالغلط، يقطع الاتصال أولاً
            if bot.voice_clients:
                for vc in bot.voice_clients:
                    await vc.disconnect()
            
            await channel.connect()
            print(f"تم الدخول إلى الروم الصوتي بنجاح: {channel.name}")
    except Exception as e:
        print(f"خطأ أثناء الدخول التلقائي: {e}")

# أمر يدوي احتياطي: لو ما دخل تلقائياً، اكتب في الشات !join وراح يدخل فوراً
@bot.command(name="join")
async def join(ctx: commands.Context):
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send("تم الدخول للروم بنجاح!")
    else:
        await ctx.send("لم يتم العثور على الروم، تأكد من الآيدي.")

bot.run("DISCORD_TOKEN")
