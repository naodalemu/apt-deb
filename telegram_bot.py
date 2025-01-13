import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set the directory for storing .deb packages
OUTPUT_BASE_DIR = os.path.expanduser("~/Desktop")

def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message and instructions."""
    update.message.reply_text(
        "Hi! Send me the name of a package (e.g., 'okular'), and I'll download it along with its dependencies for Debian."
    )

def handle_package_request(update: Update, context: CallbackContext) -> None:
    """Handles the package request."""
    package_name = update.message.text.strip()
    chat_id = update.message.chat_id

    if not package_name:
        update.message.reply_text("Please send a valid package name!")
        return

    output_dir = os.path.join(OUTPUT_BASE_DIR, f"{package_name}_debs")
    compressed_file = os.path.join(OUTPUT_BASE_DIR, f"{package_name}_package.tar.gz")

    update.message.reply_text(f"Processing your request for '{package_name}'...")

    try:
        # Step 1: Clear the apt cache
        subprocess.run(["sudo", "rm", "-rf", "/var/cache/apt/archives/*.deb"], check=True)

        # Step 2: Download the package and dependencies
        subprocess.run(["sudo", "apt-get", "install", "--download-only", "-y", package_name], check=True)

        # Step 3: Copy .deb files to the output directory
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(["sudo", "cp", "/var/cache/apt/archives/*.deb", output_dir], check=True)

        # Step 4: Create an install script
        install_script_path = os.path.join(output_dir, f"install_{package_name}.sh")
        with open(install_script_path, "w") as script_file:
            script_file.write(f"""#!/bin/bash
sudo dpkg -i *.deb
sudo apt-get install -f -y
""")
        os.chmod(install_script_path, 0o755)

        # Step 5: Compress the directory
        subprocess.run(["tar", "-czvf", compressed_file, "-C", OUTPUT_BASE_DIR, f"{package_name}_debs"], check=True)

        # Step 6: Send the compressed file to the user
        context.bot.send_document(chat_id=chat_id, document=open(compressed_file, "rb"))
        update.message.reply_text(f"The package '{package_name}' and its dependencies are ready! 🎉")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"An error occurred: {e}")
    except Exception as e:
        update.message.reply_text(f"Something went wrong: {e}")

def main():
# Get the Bot Token from Render's environment variable
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set.")
    
    # Create the Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_package_request))

    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()
