import os, datetime, discord
from discord.ext import commands, tasks
from shop import fetch_shop, build_shop_embeds

# ---- env vars ----
TOKEN = os.getenv("DISCORD_TOKEN")
SHOP_CHANNEL_ID = int(os.getenv("SHOP_CHANNEL_ID", "0"))
CREATOR_CODE = os.getenv("CREATOR_CODE", "YTBUSTY")
GUILD_ID = os.getenv("GUILD_ID")  # optional: for instant slash sync in your server

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

async def post_shop(channel: discord.abc.Messageable, full=False):
    try:
        shop_json = fetch_shop()
        embeds = build_shop_embeds(shop_json, creator_code=CREATOR_CODE, full=full)
        for e in embeds:
            await channel.send(embed=e)
    except Exception as e:
        await channel.send(f"\N{WARNING SIGN} Couldn’t fetch the shop: `{e}`")

# Daily at 00:00 UTC (Fortnite shop reset)
@tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
async def daily_shop():
    ch = bot.get_channel(SHOP_CHANNEL_ID)
    if ch:
        await post_shop(ch)

@bot.event
async def on_ready():
    # Sync slash commands
    try:
        if GUILD_ID:
            await tree.sync(guild=discord.Object(id=int(GUILD_ID)))  # instant in this server
        else:
            await tree.sync()  # global; may take longer first time
    except Exception as e:
        print("Slash sync error:", e)

    if not daily_shop.is_running():
        daily_shop.start()

    print(f"{bot.user} online.")

# Slash command: /shop [full]
@tree.command(name="shop", description="Show today’s Fortnite Item Shop")
async def shop_slash(interaction: discord.Interaction, full: bool=False):
    await interaction.response.defer(thinking=True)
    await post_shop(interaction.channel, full=full)
    await interaction.followup.send(f"Use **Creator Code {CREATOR_CODE}** \N{PURPLE HEART}")

# Optional prefix command: !shop [full]
@bot.command(name="shop")
async def shop_prefix(ctx, full: str="no"):
    flag = full.lower() in ("yes", "true", "full", "y")
    await post_shop(ctx.channel, full=flag)
    await ctx.send(f"Use **Creator Code {CREATOR_CODE}** \N{PURPLE HEART}")

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set DISCORD_TOKEN env var.")
    bot.run(TOKEN)
