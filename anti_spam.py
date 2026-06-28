import discord
from discord.ext import commands
from datetime import timedelta, datetime, timezone

# ================= CONFIG =================

HONEYPOT_CHANNEL_ID = ___  # Channel bẫy
LOG_CHANNEL_ID = ___        # Kênh log

# ==========================================

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Bỏ qua bot
        if message.author.bot:
            return

        # Chỉ xử lý channel honeypot
        if message.channel.id != HONEYPOT_CHANNEL_ID:
            return

        member = message.author

        try:
            # Xóa tin nhắn vừa gửi
            await message.delete()
 
            # Timeout 7 ngày
            timeout_until = discord.utils.utcnow() + timedelta(days=7)
            await member.timeout(
                timeout_until,
                reason="Triggered Anti-Spam Honeypot"
            )

            deleted_count = 0

            # Xóa toàn bộ tin nhắn của user trong 1 giờ gần nhất
            one_hour_ago = discord.utils.utcnow() - timedelta(hours=1)

            for channel in message.guild.text_channels:

                # Bot không có quyền đọc hoặc quản lý
                perms = channel.permissions_for(message.guild.me)

                if not perms.read_message_history or not perms.manage_messages:
                    continue

                try:
                    async for msg in channel.history(limit=500, after=one_hour_ago):

                        if msg.author.id == member.id:
                            try:
                                await msg.delete()
                                deleted_count += 1
                            except Exception:
                                pass

                except Exception:
                    continue

            # DM người dùng
            try:
                embed = discord.Embed(
                    title="❌ Anti-Spam Triggered",
                    description=(
                        "Bạn đã gửi tin nhắn vào khu vực Anti-Spam của server.\n\n"
                        "Tài khoản của bạn đã bị timeout trong **7 ngày**.\n"
                        "Nếu đây là nhầm lẫn hãy liên hệ staff."
                    ),
                    color=0xff0000
                )

                await member.send(embed=embed)

            except discord.Forbidden:
                pass

            # Gửi log
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

            if log_channel:
                embed = discord.Embed(
                    title="🚨 Honeypot Triggered",
                    color=0xff0000,
                    timestamp=datetime.now(timezone.utc)
                )

                embed.add_field(
                    name="User",
                    value=f"{member.mention}\n`{member.id}`",
                    inline=False
                )

                embed.add_field(
                    name="Action",
                    value=(
                        "⏳ Timeout: **7 ngày**\n"
                        f"🗑️ Deleted messages: **{deleted_count}**"
                    ),
                    inline=False
                )

                embed.add_field(
                    name="Channel",
                    value=message.channel.mention,
                    inline=False
                )

                await log_channel.send(embed=embed)

        except discord.Forbidden:
            print("[AntiSpam] Bot thiếu quyền.")
        except Exception as e:
            print(f"[AntiSpam] Error: {e}")


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))