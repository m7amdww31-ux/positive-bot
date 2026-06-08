# -*- coding: utf-8 -*-
"""
بوت الإيجابية والنكت - زاويتنا
يرسل رسائل إيجابية ونكت حلوة على ديسكورد
"""

import os
import random
import datetime
import asyncio

import discord
from discord import app_commands
from discord.ext import commands, tasks

try:
    from zoneinfo import ZoneInfo
    RIYADH = ZoneInfo("Asia/Riyadh")
except Exception:
    RIYADH = None

# ===================== الإعدادات =====================
TOKEN = os.getenv("DISCORD_TOKEN")

# قناة النشر التلقائي (اختياري) - حطي الـ ID في متغيرات Railway
AUTO_CHANNEL_ID = os.getenv("AUTO_CHANNEL_ID")
# ساعة النشر اليومي بتوقيت الرياض (مرة وحدة كل 24 ساعة). مثال: 9 يعني 9 الصبح
DAILY_POST_HOUR = int(os.getenv("DAILY_POST_HOUR", "9"))

# ===================== المحتوى =====================
POSITIVE_MESSAGES = [
    "صباحك/مساك خير 🌸 اليوم فرصة جديدة تستاهل تبدأها بابتسامة.",
    "أنت أقوى مما تتخيل، وكل اللي عديته من صعوبات دليل على ذلك 💪",
    "خطوة صغيرة اليوم أحسن من ألف خطة بكرة. ابدأ ولو بالقليل ✨",
    "ما عليك من نظرة الناس، طريقك انت وحدك تعرف وين يوديك 🌟",
    "خذ نفس عميق… كل شي بيمر، والأيام ما تثبت على حال ☁️",
    "كن فخور بنفسك، لأنك توك واصل لين هنا رغم كل شي 🤍",
    "النجاح مو في إنك ما تطيح، بل إنك تقوم كل مرة تطيح فيها 🚀",
    "ابتسامتك صدقة، ووجودك يفرق لناس أكثر مما تتخيل 😊",
    "ثق بنفسك، الثقة نص الطريق للهدف 🌿",
    "اليوم اللي ما تتعلم فيه شي جديد، يستاهل إنك تضيف له شي بسيط ✍️",
    "لا تقارن بدايتك بنهاية غيرك، لكل واحد توقيته الخاص ⏳",
    "أنت تستاهل كل الخير، لا تحرم نفسك منه بأفكارك السلبية 🤍",
    "أصعب الأوقات تطلع منها أقوى نسخة من نفسك 🔥",
    "كل يوم تصحى فيه نعمة، استغلها بحب وامتنان 🌻",
    "اعتنِ بنفسك اليوم: ماء، نوم كافي، وكلمة طيبة لنفسك 💧",
    "إنجازاتك الصغيرة تستاهل احتفال، لا تقلل من شأنها 🎉",
    "حلمك ما هو بعيد، هو فقط محتاج خطوات ثابتة 🌙",
    "ما يحتاج تكون مثالي، يكفي إنك تحاول بصدق 🌱",
    "العقبات مجرد محطات، مو نهاية الطريق 🛤️",
    "صدقني، أحسن أيامك لسا ما جت 🌅",
    "لا تخاف من البدايات، كل خبير كان يوم مبتدئ 📚",
    "راحتك النفسية أهم من رضا كل الناس عنك 🕊️",
    "كن لطيف مع نفسك، انت تسوي اللي تقدر عليه 🤲",
    "الفشل مو عكس النجاح، هو جزء منه 💡",
    "ابدأ يومك بنية حلوة، وبتلاحظ الفرق 🌼",
    "أنت لست وحدك، دائماً في ناس تحبك وتدعم لك 🫂",
    "حتى لو اليوم صعب، انت قدّه وزيادة 💎",
    "كل ما زاد إيمانك بنفسك، قلّ خوفك من المستقبل 🌠",
    "استمتع بالطريق، مو بس بالوصول 🚶",
    "خلك صبور مع نفسك، النمو ياخذ وقت 🌳",
]

JOKES = [
    "ليش الكتاب راح للدكتور؟ 😅 لأنه كان عنده مشاكل في الفصول!",
    "وحد سأل صاحبه: كيف تشحن جوالك بسرعة؟ قال له: أخليه يتأخر، يشحن من القلق 😂",
    "ليش الكمبيوتر راح ينام بدري؟ لأنه احتاج يعمل reset! 🖥️",
    "قالوا للبصل: ليش دايم تبكينا؟ قال: أنا طبقة فوق طبقة، عندي مشاكل عميقة 🧅😭",
    "وش يقول الحائط للحائط الثاني؟ نتقابل عند الزاوية 😆",
    "ليش السمكة ما تلعب كرة قدم؟ لأنها تخاف من الشبكة! 🐟⚽",
    "معلم سأل الطالب: وش أصعب شي في الرياضيات؟ قال: إني أحضرها 😅",
    "ليش القلم راح المستشفى؟ لأنه طاح وانكسر سنّه ✏️🏥",
    "وحد قال لصاحبه: أنا أحفظ كل أرقام جوالي… قال له كيف؟ قال: مسجلهم بالأسماء 📱😂",
    "ليش الساعة دايم تعبانة؟ لأنها طول اليوم تدور 🕐",
    "البطاطس قالت للطماطم: لا تحمرين خدودك، احنا نطبخ سوا 🍅😄",
    "ليش النملة ما تمرض أبد؟ لأن عندها anti-بادي 🐜",
    "وحد طلب من النادل ماء بدون ثلج، النادل قال: عندنا بس ماء بدون ماي 💧😆",
    "ليش الموزة راحت للدكتور؟ لأنها ما كانت تقشر زين 🍌",
    "قالوا للقهوة: ليش دايم منرفزة الصبح؟ قالت: لأني ما شربت قهوة! ☕😂",
    "وحد يدرس طب، صاحبه قال له: عالجني، قال له: روح نام، خصم 50% 🛌",
    "ليش الثلاجة منعزلة؟ لأنها دايم باردة مع الكل 🧊",
    "المفتاح قال للقفل: انت بس اللي تفهمني 🔑😍",
    "ليش الطباخ ما يكذب؟ لأنه دايم يطلع الصدق من القدر 🍲😄",
    "وحد سأل: ليش الجمل ما يلعب شطرنج؟ قال: لأنه دايم يحب الصحراء مو المربعات 🐫",
    "قالوا للورقة: ليش ساكتة؟ قالت: لأني مكتوب علي ما أتكلم 📄😆",
    "ليش الباص دايم متأخر؟ لأنه يحب يخلي الكل ينتظره عشان يحس بأهميته 🚌",
    "وحد طلب شاهي حار، النادل قال: تأكد؟ قال: إيه، أنا قوي 🔥😂",
    "ليش الشمعة حزينة؟ لأن كل يوم تنطفئ أحلامها 🕯️",
    "البطة قالت للوزة: تعالي نسبح، قالت لها: ما أعرف، أنا بطّالة 🦆😄",
    "ليش النجوم ما تنام؟ لأنها تشتغل ليلي 🌟",
    "وحد قال: عندي ذاكرة قوية بس… نسيت وش كنت أبي أقول 🧠😂",
    "ليش الجوال يسخن؟ لأنه يحمل هموم صاحبه طول اليوم 📲",
    "قالوا للمطر: وقّف شوي، قال: أنا نازل من فوق، ما أقدر أوقف 🌧️😆",
    "ليش الكرسي ما يمشي؟ لأنه دايم منتظر أحد يجلس عليه 🪑",
]

# ===================== البوت =====================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="#", intents=intents)


def make_embed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="زاويتنا 🤍")
    return embed


@bot.event
async def on_ready():
    print(f"✅ البوت شغال باسم: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ تم مزامنة {len(synced)} أمر سلاش")
    except Exception as e:
        print(f"⚠️ خطأ في مزامنة الأوامر: {e}")
    if AUTO_CHANNEL_ID and not auto_post.is_running():
        auto_post.start()
        print("✅ النشر التلقائي مفعّل")


# ---------- أوامر السلاش ----------
@bot.tree.command(name="ايجابية", description="رسالة إيجابية تفرّح يومك 🌸")
async def positive_slash(interaction: discord.Interaction):
    msg = random.choice(POSITIVE_MESSAGES)
    await interaction.response.send_message(
        embed=make_embed("✨ رسالة إيجابية", msg, 0x7DD3FC)
    )


@bot.tree.command(name="نكتة", description="نكتة حلوة تضحكك 😄")
async def joke_slash(interaction: discord.Interaction):
    joke = random.choice(JOKES)
    await interaction.response.send_message(
        embed=make_embed("😂 نكتة", joke, 0xFDE047)
    )


@bot.tree.command(name="مساعدة", description="عرض كل الأوامر")
async def help_slash(interaction: discord.Interaction):
    desc = (
        "**/ايجابية** — رسالة إيجابية تفرّح يومك 🌸\n"
        "**/نكتة** — نكتة حلوة تضحكك 😄\n"
        "**/مساعدة** — عرض هالقائمة\n\n"
        "تقدرين كمان تستخدمين: `#ايجابية` و `#نكتة`"
    )
    await interaction.response.send_message(
        embed=make_embed("📋 الأوامر", desc, 0xA78BFA)
    )


# ---------- أوامر البادئة (!) ----------
@bot.command(name="ايجابية")
async def positive_prefix(ctx):
    msg = random.choice(POSITIVE_MESSAGES)
    await ctx.send(embed=make_embed("✨ رسالة إيجابية", msg, 0x7DD3FC))


@bot.command(name="نكتة")
async def joke_prefix(ctx):
    joke = random.choice(JOKES)
    await ctx.send(embed=make_embed("😂 نكتة", joke, 0xFDE047))


# ---------- النشر التلقائي (مرة وحدة كل 24 ساعة) ----------
@tasks.loop(minutes=1)
async def auto_post():
    if not AUTO_CHANNEL_ID:
        return
    now = datetime.datetime.now(RIYADH) if RIYADH else datetime.datetime.now()
    # ننشر فقط مرة وحدة باليوم: عند الساعة المحددة والدقيقة 0
    if now.hour != DAILY_POST_HOUR or now.minute != 0:
        return

    channel = bot.get_channel(int(AUTO_CHANNEL_ID))
    if channel is None:
        return

    # رسالة إيجابية + نكتة في نشر يومي واحد
    msg = random.choice(POSITIVE_MESSAGES)
    joke = random.choice(JOKES)
    await channel.send(embed=make_embed("🌸 رسالة اليوم", msg, 0x7DD3FC))
    await channel.send(embed=make_embed("😂 نكتة اليوم", joke, 0xFDE047))


@auto_post.before_loop
async def before_auto_post():
    await bot.wait_until_ready()


# ===================== التشغيل =====================
if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("⚠️ لازم تحطين DISCORD_TOKEN في متغيرات Railway")
    bot.run(TOKEN)
