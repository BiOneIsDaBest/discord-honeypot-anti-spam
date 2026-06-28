🛡️ Discord Honeypot Anti-Spam Cog

A lightweight Discord.py 2.x Cog designed to automatically detect compromised accounts and stop mass spam attacks.

This Cog creates a honeypot channel: if a user sends any message in that channel, the bot will instantly:

* ⏳ Timeout the user for 7 days
* 🗑️ Delete all messages sent by that user during the last 1 hour
* 📩 Optionally notify the user via DM
* 📦 Send a detailed log to a log channel

Perfect for communities frequently targeted by:

* Token-stealer victims
* Crypto spam bots
* Compromised Discord accounts
* Automated invite spam

⸻

✨ Features

✅ Honeypot channel detection

✅ Automatic 7-day timeout

✅ Bulk delete recent messages

✅ Detailed moderation logs

✅ Lightweight and easy to integrate

✅ Built for Discord.py 2.x

⸻

📂 Project Structure

project/
│
├── main.py
├── .env
├── requirements.txt
│
└── cogs/
    └── anti_spam.py

Simply place:

anti_spam.py

inside your:

cogs/

folder and load it as a normal Cog.

⸻

⚙️ Configuration

Inside anti_spam.py edit:

HONEYPOT_CHANNEL_ID = 123456789012345678
LOG_CHANNEL_ID = 123456789012345678

Optional:

WHITELIST_USERS = [YOUR_USER_ID]

⸻

🔒 Required Bot Permissions

The bot requires:

* View Channels
* Read Message History
* Manage Messages
* Moderate Members

The bot role must also be placed above normal member roles.

⸻

🚀 Installation

pip install -r requirements.txt

Load the Cog:

await bot.load_extension("cogs.anti_spam")

⸻

🇻🇳 Tiếng Việt

Đây là Cog chống spam dành cho Discord.py 2.x sử dụng cơ chế Honeypot Channel.

Khi người dùng gửi bất kỳ tin nhắn nào vào kênh bẫy:

* ⏳ Bot sẽ timeout người dùng trong 7 ngày
* 🗑️ Xóa toàn bộ tin nhắn mà người đó đã gửi trong 1 giờ gần nhất
* 📩 Có thể gửi cảnh báo qua DM
* 📦 Ghi log đầy đủ vào kênh quản trị

Tính năng này đặc biệt hữu ích để ngăn chặn:

* Tài khoản Discord bị đánh cắp token
* Spam crypto
* Spam server invite
* Account bị nhiễm malware

⸻

📸 Recommended Usage

Create a channel similar to:

#verification
#verify-here
#human-check

Place a clear warning message inside:

⚠️ Do not send messages in this channel. Any message sent here will result in an automatic timeout.

Most compromised accounts and spam bots will still attempt to send messages, allowing the bot to automatically detect and isolate them.

⸻

🛡️ Copyright

Copyright © BiOneIsDaBest

📌 If you use or modify this project, please provide proper credit or contact:

Discord: [BiOneIsDaBest](https://discord.com/users/1146990393167200276)
