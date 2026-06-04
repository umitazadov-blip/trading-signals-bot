#!/usr/bin/env python3
"""
Trading Signals Bot - Main Entry Point
Telegram bot for trading analysis with technical indicators
"""

import logging
from telegram.ext import Application, CommandHandler, ContextTypes
from utils.logger import setup_logger
from utils.helpers import get_config
from bot.commands import (
    start, help_command, analyze_command, 
    portfolio_command, stats_command, status_command
)

logger = setup_logger(__name__)

def main():
    """Start the bot."""
    config = get_config()
    
    # Create bot application
    application = Application.builder().token(config['telegram_token']).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyze", analyze_command))
    application.add_handler(CommandHandler("portfolio", portfolio_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Start polling
    logger.info("🤖 Bot başlatılıyor...")
    application.run_polling(allowed_updates=['message', 'callback_query'])

if __name__ == '__main__':
    main()
