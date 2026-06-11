import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

class YozuTelegramBot:
    def __init__(self, brain, memory, voice_callback=None):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.brain = brain
        self.memory = memory
        self.voice_callback = voice_callback
        self.application = None

    async def start(self):
        if not self.token:
            print("TELEGRAM_TOKEN not found in .env. Telegram bot disabled.")
            return

        self.application = ApplicationBuilder().token(self.token).build()

        start_handler = CommandHandler('start', self._start_command)
        msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self._handle_message)

        self.application.add_handler(start_handler)
        self.application.add_handler(msg_handler)

        print("Telegram bot starting...")
        await self.application.initialize()
        await self.application.start_polling()
        await self.application.updater.start_polling()

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Yozu! Your desktop companion. How can I help you today?")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        print(f"Telegram message received: {user_text}")

        # Query the brain (Note: In a full implementation, we'd pass tool instances here too)
        response = self.brain.query(f"User via Telegram: {user_text}")

        # Save to memory
        self.memory.save_thought("Telegram Chat", f"User: {user_text}\nYozu: {response}", tags=["telegram", "chat"])

        # Speak locally if callback provided (optional based on user preference)
        if self.voice_callback:
            self.voice_callback(response)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    async def stop(self):
        if self.application:
            await self.application.stop()
            await self.application.shutdown()
