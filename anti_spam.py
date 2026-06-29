import discord
from discord.ext import commands
from datetime import timedelta, datetime, timezone

# ================= CONFIG =================

HONEYPOT_CHANNEL_IDS = ( xxx, xxx, ) # Channel bẫy — thay bằng ID thật 
LOG_CHANNEL_ID = xxx # Kênh log

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
        if message.channel.id not in HONEYPOT_CHANNEL_IDS:
            return

        member = message.author

        missing_perms = []  # Danh sách quyền thiếu để log

        try:
            # Xóa tin nhắn vừa gửi
            try:
                await message.delete()
            except discord.Forbidden:
                missing_perms.append(f"⚠️ Thiếu quyền **Manage Messages** tại {message.channel.mention} — không thể xóa tin nhắn honeypot")
                print(f"[AntiSpam] Thiếu quyền Manage Messages tại #{message.channel.name}")

            # Timeout 7 ngày
            try:
                timeout_until = discord.utils.utcnow() + timedelta(days=7)
                await member.timeout(
                    timeout_until,
                    reason="Triggered Anti-Spam Honeypot"
                )
            except discord.Forbidden:
                missing_perms.append(f"⚠️ Thiếu quyền **Moderate Members** — không thể timeout {member.mention}")
                print(f"[AntiSpam] Thiếu quyền Moderate Members — không thể timeout {member}")

            deleted_count = 0

            # Xóa toàn bộ tin nhắn của user trong 1 giờ gần nhất
            one_hour_ago = discord.utils.utcnow() - timedelta(hours=1)

            for channel in message.guild.text_channels:

                perms = channel.permissions_for(message.guild.me)

                # Log cụ thể quyền nào thiếu tại kênh nào
                if not perms.read_message_history and not perms.manage_messages:
                    missing_perms.append(f"⚠️ Thiếu quyền **Read Message History** và **Manage Messages** tại {channel.mention}")
                    print(f"[AntiSpam] Thiếu quyền Read Message History và Manage Messages tại #{channel.name}")
                    continue
                elif not perms.read_message_history:
                    missing_perms.append(f"⚠️ Thiếu quyền **Read Message History** tại {channel.mention}")
                    print(f"[AntiSpam] Thiếu quyền Read Message History tại #{channel.name}")
                    continue
                elif not perms.manage_messages:
                    missing_perms.append(f"⚠️ Thiếu quyền **Manage Messages** tại {channel.mention}")
                    print(f"[AntiSpam] Thiếu quyền Manage Messages tại #{channel.name}")
                    continue

                try:
                    async for msg in channel.history(limit=500, after=one_hour_ago):

                        if msg.author.id == member.id:
                            try:
                                await msg.delete()
                                deleted_count += 1
                            except discord.Forbidden:
                                missing_perms.append(f"⚠️ Thiếu quyền **Manage Messages** tại {channel.mention} — không thể xóa tin nhắn")
                                print(f"[AntiSpam] Thiếu quyền Manage Messages tại #{channel.name} — không thể xóa tin nhắn")
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

                # Thêm field cảnh báo quyền thiếu (nếu có)
                if missing_perms:
                    # Giới hạn 1024 ký tự (limit của embed field)
                    perms_text = "\n".join(missing_perms)
                    if len(perms_text) > 1024:
                        perms_text = perms_text[:1021] + "..."

                    embed.add_field(
                        name="🔒 Thiếu quyền",
                        value=perms_text,
                        inline=False
                    )

                await log_channel.send(embed=embed)

        except Exception as e:
            print(f"[AntiSpam] Error: {e}")


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
