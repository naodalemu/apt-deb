# Telegram Bot for Debian Package Downloads

This Telegram bot allows users to request Debian package downloads along with their dependencies. The bot packages the `.deb` files and includes an installation script, compresses them into a `.tar.gz` archive, and sends the file back to the user.

---

## Features

- Download Debian packages along with all their dependencies.
- Automatically create an installation script for easy setup.
- Compress the package and its dependencies for easy sharing.
- Respond to user requests via Telegram.
- Supports dynamic package names.

---

## Prerequisites

1. **Telegram Bot Token**
   - Create a bot via [BotFather](https://core.telegram.org/bots#botfather) and obtain the API token.

2. **System Requirements**
   - Python 3.6 or higher.
   - Linux-based system with `apt-get`.
   - Telegram API library (`python-telegram-bot`).

3. **Dependencies**
   - Install required Python libraries:
     ```bash
     pip install python-telegram-bot
     ```
