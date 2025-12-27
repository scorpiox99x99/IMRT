import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv

# --- LOAD TOKEN ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# --- CHANNEL & ROLE SETTINGS ---
WELCOME_CHANNEL_ID = 1434506938141638666  # your main server's welcome channel
VERIFY_CHANNEL_ID = 1432336229776490567   # your main server's verify channel
VERIFIED_ROLE_NAME = "Verified ✅"

# --- INTENTS ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- VERIFICATION BUTTON ---
class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Verified ✅", style=discord.ButtonStyle.success, custom_id="verify_button"))

# --- EVENT: WHEN BOT IS READY ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    # Optional: run this setup only ONCE for your main server
    guild = bot.get_guild(1426503725677281324)  # replace with your main server's ID
    if guild:
        channel = guild.get_channel(VERIFY_CHANNEL_ID)
        if channel:
            # Prevent duplicate embeds (don’t resend if message already exists)
            async for message in channel.history(limit=10):
                if message.author == bot.user and message.embeds and "Verify" in message.embeds[0].title:
                    print("🔸 Verify embed already exists, skipping.")
                    return

            embed = discord.Embed(
                title="🔒 Verify to Unlock the Server!",
                description="Click the **Verify** button below to gain full access to the server.",
                color=discord.Color.gold()
            )
            embed.set_image(url="https://i.ibb.co/qR3vH6v/verify-banner.gif")
            embed.set_footer(text="Server Security System 🛡️")
            await channel.send(embed=embed, view=VerifyView())

# --- EVENT: WHEN MEMBER JOINS ---
@bot.event
async def on_member_join(member: discord.Member):
    # ✅ Only run for humans
    if member.bot:
        return

    guild = member.guild
    if guild.id != 1429235488564183220:
        return  # ignore joins on other servers

    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)

    # --- DM MESSAGE ---
    try:
        dm_embed = discord.Embed(
            title=f"👋 Welcome to {guild.name}!",
            description=f"Hey {member.mention}! We're thrilled to have you here 💫\nHead to the verification channel and click **Verify** to access all chats.",
            color=discord.Color.blurple()
        )
        dm_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        dm_embed.set_footer(text="Enjoy your stay 💖")
        await member.send(embed=dm_embed)
    except:
        pass

    # --- WELCOME MESSAGE ---
    if welcome_channel:
        embed = discord.Embed(
            title="🎉 A New Member Has Arrived!",
            description=(
                f"Welcome {member.mention} to **{guild.name}**!\n\n"
                "We’re excited to have you here! 💥\n"
                "Please head to #verify and get verified to access all channels!"
            ),
            color=discord.Color.dark_theme()  # Black-like embed color
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="https://i.ibb.co/sqn2g2B/welcome-banner-gradient.gif")
        embed.set_footer(text=f"Member Count: {guild.member_count} ✨")
        await welcome_channel.send(embed=embed)

# --- EVENT: WHEN VERIFY BUTTON IS CLICKED ---
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data and interaction.data.get("custom_id") == "verify_button":
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=VERIFIED_ROLE_NAME)

        if not role:
            role = await guild.create_role(name=VERIFIED_ROLE_NAME, reason="Created for verification system")

        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ You’ve been verified! Welcome aboard 🎉", ephemeral=True)

# --- RUN BOT ---

bot.run(TOKEN)


