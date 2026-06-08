# بوت الإيجابية والنكت 🌸😂

بوت ديسكورد يرسل رسائل إيجابية ونكت حلوة لسيرفر **زاويتنا**.

## ✨ المميزات
- `/ايجابية` أو `#ايجابية` — رسالة إيجابية تفرّح يومك
- `/نكتة` أو `#نكتة` — نكتة حلوة تضحكك
- `/مساعدة` — عرض كل الأوامر
- نشر تلقائي يومي اختياري (رسالة إيجابية + نكتة مرة كل ٢٤ ساعة)

---

## 📦 خطوات الرفع على GitHub

1. ادخلي حسابك `m7amdww31-ux` على GitHub
2. سوّي Repository جديد (مثلاً باسم `positive-bot`)
3. ارفعي هالملفات عن طريق **Add file → Upload files**:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
4. اضغطي **Commit changes**

---

## 🚀 خطوات النشر على Railway

1. ادخلي [railway.app](https://railway.app) → **New Project**
2. اختاري **Deploy from GitHub repo** → اختاري الريبو اللي رفعتيه
3. روحي على **Variables** وضيفي المتغيرات التالية:

| المتغير | القيمة |
|---|---|
| `DISCORD_TOKEN` | توكن البوت من Discord Developer Portal |
| `MISE_PYTHON_GITHUB_ATTESTATIONS` | `false` |

### (اختياري) للنشر التلقائي اليومي (مرة كل ٢٤ ساعة):

| المتغير | القيمة | الشرح |
|---|---|---|
| `AUTO_CHANNEL_ID` | ID القناة | القناة اللي بينشر فيها |
| `DAILY_POST_HOUR` | `9` | ساعة النشر اليومي بتوقيت الرياض (٠–٢٣) |

4. Railway بينشر تلقائي. تابعي **Deployments → Logs** لين تشوفين:
   `✅ البوت شغال`

---

## 🔑 وين أجيب التوكن؟
1. روحي [discord.com/developers/applications](https://discord.com/developers/applications)
2. **New Application** → اكتبي اسم البوت
3. من القائمة الجانبية **Bot** → **Reset Token** → انسخي التوكن
4. تحت **Privileged Gateway Intents** فعّلي **MESSAGE CONTENT INTENT**
5. من **OAuth2 → URL Generator**: اختاري `bot` و `applications.commands`، وصلاحيات `Send Messages`، وادعي البوت لسيرفرك

---

## 🆔 كيف أطلع ID القناة؟
في ديسكورد: **الإعدادات → Advanced → فعّلي Developer Mode**، بعدها كليك يمين على القناة → **Copy Channel ID**.
