# GalacticModz Fortnite Shop Bot (EFS-like)
Posts the Fortnite Item Shop daily at reset (00:00 UTC) and on-demand via `/shop` or `!shop`.
Always promotes your Creator Code.

## Features
- Auto-post item shop at 00:00 UTC (8 PM ET)
- `/shop` slash command (with optional `full` flag)
- Optional `!shop` prefix command
- Creator Code branding via env var

## Files
- `main.py` — bot entrypoint + commands and scheduler
- `shop.py` — fetches shop data and builds Discord embeds
- `requirements.txt` — Python dependencies
- `Procfile` — tells Railway to run `python main.py` as a worker

## Setup — Discord
1. Create a bot in the Discord Developer Portal.
2. Scopes: `bot`, `applications.commands`. Permissions: `Send Messages`, `Embed Links`.
3. Invite it to your server.

## Environment Variables
- `DISCORD_TOKEN` — your bot token (REQUIRED)
- `SHOP_CHANNEL_ID` — numeric channel ID to auto-post shop (REQUIRED)
- `CREATOR_CODE` — defaults to `YTBUSTY`
- `GUILD_ID` — optional; your server ID for instant slash sync

## Railway Deploy
1. Push this folder to GitHub.
2. In Railway: New Project → Deploy from GitHub.
3. Add variables: `DISCORD_TOKEN`, `SHOP_CHANNEL_ID`, `CREATOR_CODE`, (optional) `GUILD_ID`.
4. Deploy.

## Test
- Run `/shop` in your Discord to fetch the current shop.
- The bot will auto-post at 00:00 UTC daily to `SHOP_CHANNEL_ID`.
