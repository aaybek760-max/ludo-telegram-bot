import os
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN =8251349766:AAHYVUn9f3pet4CCKYU
wVxtFi6m__OtD2Cg os.environ.get("BOT_TOKEN")

games = {}


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Ludo bot is running!")

    def log_message(self, format, *args):
        pass


def start_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


def game_text(game):
    text = "🎲 LUDO O'YINI\n\n"

    if not game["players"]:
        return text + "Hozircha o‘yinchilar yo‘q."

    for i, player in enumerate(game["players"]):
        text += f"{i + 1}. {player['name']} — {player['color']}\n"

    text += "\n"

    if game["started"]:
        current = game["players"][game["turn"]]
        text += f"🎯 Navbat: {current['name']}\n"
        text += "🎲 Kubikni tashlang!"
    else:
        text += f"👥 O‘yinchilar: {len(game['players'])}/4\n"
        text += "Kamida 2 kishi kerak."

    return text


def keyboard(game):
    buttons = []

    if not game["started"] and len(game["players"]) < 4:
        buttons.append([
            InlineKeyboardButton("➕ O‘yinga qo‘shilish", callback_data="join")
        ])

    if game["started"]:
        buttons.append([
            InlineKeyboardButton("🎲 KUBIK TASHLASH", callback_data="roll")
        ])

    buttons.append([
        InlineKeyboardButton("❌ O‘yinni tugatish", callback_data="end")
    ])

    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Ludo Botga xush kelibsiz!\n\n"
        "O‘yin boshlash uchun:\n"
        "👉 /ludo\n\n"
        "Keyin boshqa o‘yinchilar qo‘shiladi.",
        parse_mode="Markdown",
    )


async def ludo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    games[chat_id] = {
        "players": [],
        "started": False,
        "turn": 0,
    }

    await update.message.reply_text(
        game_text(games[chat_id]),
        reply_markup=keyboard(games[chat_id]),
        parse_mode="Markdown",
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id

    if chat_id not in games:
        await query.edit_message_text("❌ Avval /ludo buyrug‘ini yuboring.")
        return

    game = games[chat_id]

    if query.data == "join":
        if game["started"]:
            await query.answer("O‘yin allaqachon boshlandi!", show_alert=True)
            return

        user_id = query.from_user.id

        for p in game["players"]:
            if p["id"] == user_id:
                await query.answer("Siz allaqachon o‘yindasiz!", show_alert=True)
                return

        colors = ["🔴 Qizil", "🔵 Ko‘k", "🟢 Yashil", "🟡 Sariq"]

        game["players"].append({
            "id": user_id,
            "name": query.from_user.first_name,
            "color": colors[len(game["players"])],
            "score": 0,
        })

        if len(game["players"]) >= 2:
            game["started"] = True

        await query.edit_message_text(
            game_text(game),
            reply_markup=keyboard(game),
            parse_mode="Markdown",
        )

    elif query.data == "roll":
        if not game["started"]:
            await query.answer(
                "Kamida 2 ta o‘yinchi kerak!",
                show_alert=True,
            )
            return

        current = game["players"][game["turn"]]
