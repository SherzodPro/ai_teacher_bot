#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ai_teacher_uz_bot — Qoraqalpoq tilindagi AI o'qituvchi boti
O'quvchilar va o'qituvchilar uchun video darslik boti
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# =============================================
# BOT TOKENINI SHU YERGA QO'YING
# =============================================
BOT_TOKEN = "8757209075:AAHU9xkw7Wqj_BxVDudU91brbob4efpZK98"

# =============================================
# VIDEO DARSLIKLAR MA'LUMOTLARI
# Keyin ko'proq qo'shib borish mumkin!
# =============================================
VIDEO_DARSLIKLAR = {
    "matematika": {
        "nomi": "📐 Matematika",
        "mavzular": {
            "algebra": {
                "nomi": "Algebra",
                "videolar": [
                    {"sarlavha": "Teńlemeler (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE1", "sinf": "9"},
                    {"sarlavha": "Kvadrat teńlemeler (2-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE2", "sinf": "9"},
                    {"sarlavha": "Progressiyalar (3-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE3", "sinf": "10"},
                ]
            },
            "geometriya": {
                "nomi": "Geometriya",
                "videolar": [
                    {"sarlavha": "Uchburchaklar (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE4", "sinf": "9"},
                    {"sarlavha": "Aylana hám tógereк (2-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE5", "sinf": "10"},
                ]
            }
        }
    },
    "fizika": {
        "nomi": "⚡ Fizika",
        "mavzular": {
            "mexanika": {
                "nomi": "Mexanika",
                "videolar": [
                    {"sarlavha": "Newton nızamları (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE6", "sinf": "9"},
                    {"sarlavha": "Energiya hám jumıs (2-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE7", "sinf": "10"},
                ]
            },
            "elektr": {
                "nomi": "Elektr",
                "videolar": [
                    {"sarlavha": "Elektr togi (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE8", "sinf": "10"},
                ]
            }
        }
    },
    "kimyo": {
        "nomi": "🧪 Kimyo",
        "mavzular": {
            "umumiy": {
                "nomi": "Umumiy kimyo",
                "videolar": [
                    {"sarlavha": "Atom dúzilisi (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE9", "sinf": "9"},
                    {"sarlavha": "Kimyalıq reaksiyalar (2-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE10", "sinf": "10"},
                ]
            }
        }
    },
    "biologiya": {
        "nomi": "🌿 Biologiya",
        "mavzular": {
            "umumiy": {
                "nomi": "Umumiy biologiya",
                "videolar": [
                    {"sarlavha": "Hujayra dúzilisi (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE11", "sinf": "9"},
                    {"sarlavha": "Genetika tiykarları (2-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE12", "sinf": "11"},
                ]
            }
        }
    },
    "informatika": {
        "nomi": "💻 Informatika",
        "mavzular": {
            "dasturlash": {
                "nomi": "Dasturlash",
                "videolar": [
                    {"sarlavha": "Python tiykarları (1-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE13", "sinf": "10"},
                    {"sarlavha": "Algoritm hám dastur (2-dáris)", "link": "https://youtube.com/watch?v=EXAMPLE14", "sinf": "9"},
                ]
            }
        }
    }
}

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# =============================================
# /start buyrug'i
# =============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("📚 Video dárslikler", callback_data="video_menu")],
        [InlineKeyboardButton("👨‍🎓 Oqıwshı", callback_data="rol_oquvchi"),
         InlineKeyboardButton("👨‍🏫 Mugállim", callback_data="rol_mugallim")],
        [InlineKeyboardButton("ℹ️ Kómek", callback_data="yordam")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    matn = (
        f"👋 Sálem, {user.first_name}!\n\n"
        "🤖 Men — *AI Mugállim boti*\n"
        "Qoraqalpaqstan mektep oqıwshıları hám mugállimler ushın islengen.\n\n"
        "📺 *Ne islew múmkin:*\n"
        "• Pán boyınsha video dárslikler kóriw\n"
        "• Mavzu boyınsha dáris tabıw\n"
        "• Klass boyınsha materiallar alıw\n\n"
        "Tómendegi túymeni basıń 👇"
    )
    
    await update.message.reply_text(matn, reply_markup=reply_markup, parse_mode='Markdown')


# =============================================
# Video darsliklar menyusi
# =============================================
async def video_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for fan_key, fan_data in VIDEO_DARSLIKLAR.items():
        keyboard.append([InlineKeyboardButton(
            fan_data["nomi"], 
            callback_data=f"fan_{fan_key}"
        )])
    keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data="bosh_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📚 *Pándi tańlań:*\n\nQaysi pán boyınsha video dárislik kórgińiz keledi?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# =============================================
# Fan tanlash — mavzularni ko'rsatish
# =============================================
async def fan_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    fan_key = query.data.replace("fan_", "")
    fan_data = VIDEO_DARSLIKLAR.get(fan_key, {})
    
    if not fan_data:
        await query.edit_message_text("❌ Pán tabılmadı.")
        return
    
    keyboard = []
    for mavzu_key, mavzu_data in fan_data["mavzular"].items():
        keyboard.append([InlineKeyboardButton(
            f"📖 {mavzu_data['nomi']}",
            callback_data=f"mavzu_{fan_key}_{mavzu_key}"
        )])
    keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data="video_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{fan_data['nomi']} — *Mavzu tańlań:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# =============================================
# Mavzu tanlash — videolarni ko'rsatish
# =============================================
async def mavzu_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    parts = query.data.replace("mavzu_", "").split("_", 1)
    fan_key = parts[0]
    mavzu_key = parts[1]
    
    fan_data = VIDEO_DARSLIKLAR.get(fan_key, {})
    mavzu_data = fan_data.get("mavzular", {}).get(mavzu_key, {})
    
    if not mavzu_data:
        await query.edit_message_text("❌ Mavzu tabılmadı.")
        return
    
    matn = f"🎬 *{fan_data['nomi']} — {mavzu_data['nomi']}*\n\n"
    matn += "Tómendegi video dársliklerdi kórińiz:\n\n"
    
    keyboard = []
    for i, video in enumerate(mavzu_data["videolar"]):
        matn += f"▶️ {i+1}. {video['sarlavha']} ({video['sinf']}-klass)\n"
        keyboard.append([InlineKeyboardButton(
            f"▶️ {video['sarlavha']}",
            url=video["link"]
        )])
    
    keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data=f"fan_{fan_key}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(matn, reply_markup=reply_markup, parse_mode='Markdown')


# =============================================
# Rol tanlash
# =============================================
async def rol_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "rol_oquvchi":
        matn = (
            "👨‍🎓 *Oqıwshı rejimi*\n\n"
            "Siz oqıwshı retinde:\n"
            "✅ Video dárslikler kóriwińiz múmkin\n"
            "✅ Mavzu boyınsha izlew múmkin\n"
            "✅ Klass boyınsha materiallar alıwıńız múmkin\n\n"
            "📚 /video — Video dársliklerge ótiw\n"
            "🔍 /izle — Mavzu izlew"
        )
    else:
        matn = (
            "👨‍🏫 *Mugállim rejimi*\n\n"
            "Siz mugállim retinde:\n"
            "✅ Video dárslikler kóriwińiz múmkin\n"
            "✅ Oqıwshılarǵa link júberiw múmkin\n"
            "✅ Materiallar qosıw ushın @ai_teacher_admin ga jazıń\n\n"
            "📚 /video — Video dársliklerge ótiw"
        )
    
    keyboard = [[InlineKeyboardButton("⬅️ Bas menyu", callback_data="bosh_menu")]]
    await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


# =============================================
# Yordam
# =============================================
async def yordam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    matn = (
        "ℹ️ *Kómek*\n\n"
        "🤖 *@ai_teacher_uz_bot* — Qoraqalpaqstan mektep oqıwshıları ushın\n\n"
        "*Buyruqlar:*\n"
        "/start — Bas menyu\n"
        "/video — Video dárslikler\n"
        "/izle [mavzu] — Mavzu boyınsha izlew\n\n"
        "*Mısalı:* /izle algebra\n\n"
        "❓ Sorawlar ushın: @ai_teacher_admin"
    )
    
    keyboard = [[InlineKeyboardButton("⬅️ Artqa", callback_data="bosh_menu")]]
    await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


# =============================================
# Bosh menu
# =============================================
async def bosh_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📚 Video dárslikler", callback_data="video_menu")],
        [InlineKeyboardButton("👨‍🎓 Oqıwshı", callback_data="rol_oquvchi"),
         InlineKeyboardButton("👨‍🏫 Mugállim", callback_data="rol_mugallim")],
        [InlineKeyboardButton("ℹ️ Kómek", callback_data="yordam")],
    ]
    
    await query.edit_message_text(
        "🏠 *Bas menyu*\n\nNe islegińiz keledi?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


# =============================================
# /video buyrug'i
# =============================================
async def video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for fan_key, fan_data in VIDEO_DARSLIKLAR.items():
        keyboard.append([InlineKeyboardButton(
            fan_data["nomi"],
            callback_data=f"fan_{fan_key}"
        )])
    
    await update.message.reply_text(
        "📚 *Pándi tańlań:*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


# =============================================
# /izle buyrug'i — mavzu qidirish
# =============================================
async def izle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🔍 Mavzu jazıń.\n*Mısalı:* /izle algebra",
            parse_mode='Markdown'
        )
        return
    
    sorov = " ".join(context.args).lower()
    natijalar = []
    
    for fan_key, fan_data in VIDEO_DARSLIKLAR.items():
        for mavzu_key, mavzu_data in fan_data["mavzular"].items():
            for video in mavzu_data["videolar"]:
                if sorov in video["sarlavha"].lower() or sorov in mavzu_data["nomi"].lower():
                    natijalar.append({
                        "sarlavha": video["sarlavha"],
                        "fan": fan_data["nomi"],
                        "link": video["link"],
                        "sinf": video["sinf"]
                    })
    
    if natijalar:
        matn = f"🔍 *'{sorov}'* boyınsha nátiyje:\n\n"
        keyboard = []
        for n in natijalar[:5]:
            matn += f"▶️ {n['sarlavha']} — {n['fan']} ({n['sinf']}-klass)\n"
            keyboard.append([InlineKeyboardButton(f"▶️ {n['sarlavha']}", url=n["link"])])
        
        await update.message.reply_text(matn, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    else:
        await update.message.reply_text(
            f"😔 *'{sorov}'* boyınsha video tabılmadı.\n\n/video — Barlıq dársliklerdi kóriw",
            parse_mode='Markdown'
        )


# =============================================
# Oddiy xabarlar
# =============================================
async def xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.lower()
    
    # Oddiy savollarga javob
    if any(w in matn for w in ["salom", "sálem", "привет", "hello"]):
        javob = "👋 Sálem! /start basıń yáki /video yazıń 📚"
    elif any(w in matn for w in ["raxmet", "rahmet", "спасибо", "thanks"]):
        javob = "😊 Keriginiz joq! Barlıq waqıt kómekke tayarman 🤖"
    elif any(w in matn for w in ["kim", "ne", "qanday"]):
        javob = "🤖 Men — AI Mugállim boti!\n/start — Barlıq mümkinshiliklerdi kóriw"
    else:
        javob = (
            "📚 Video dárislik izleyapsızba?\n\n"
            "• /video — Pán tańlaw\n"
            "• /izle algebra — Mavzu izlew\n"
            "• /start — Bas menyu"
        )
    
    await update.message.reply_text(javob)


# =============================================
# ASOSIY FUNKSIYA
# =============================================
def main():
    if BOT_TOKEN == "TOKEN_INI_BU_YERGE_QOY":
        print("❌ XATO: Bot tokenini qo'ying!")
        print("1. @BotFather ga yozing")
        print("2. /newbot yoki /mybot")
        print("3. Tokenni nusxalab BOT_TOKEN ga qo'ying")
        return
    
    print("🚀 AI Mugállim boti ishga tushmoqda...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Buyruqlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", video_command))
    app.add_handler(CommandHandler("izle", izle_command))
    
    # Tugmalar
    app.add_handler(CallbackQueryHandler(video_menu, pattern="^video_menu$"))
    app.add_handler(CallbackQueryHandler(fan_tanlash, pattern="^fan_"))
    app.add_handler(CallbackQueryHandler(mavzu_tanlash, pattern="^mavzu_"))
    app.add_handler(CallbackQueryHandler(rol_tanlash, pattern="^rol_"))
    app.add_handler(CallbackQueryHandler(yordam, pattern="^yordam$"))
    app.add_handler(CallbackQueryHandler(bosh_menu, pattern="^bosh_menu$"))
    
    # Oddiy xabarlar
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))
    
    print("✅ Bot muvaffaqiyatli ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
