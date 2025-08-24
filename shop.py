import requests, discord

API_URL = "https://fortnite-api.com/v2/shop/br/combined"

def fetch_shop():
    r = requests.get(API_URL, headers={"User-Agent": "GalacticModz-EFS-Clone/1.0"}, timeout=20)
    r.raise_for_status()
    return r.json()

def build_shop_embeds(shop_json, creator_code="YTBUSTY", full=False):
    data = shop_json.get("data", {})
    sections = [
        ("Featured", data.get("featured", {}).get("entries", [])),
        ("Daily",    data.get("daily", {}).get("entries", [])),
    ]
    embeds = []
    for title, entries in sections:
        if not entries:
            continue
        chunk_size = 8 if full else 5  # discord embed has field limits; keep tidy
        for i in range(0, len(entries), chunk_size):
            chunk = entries[i:i+chunk_size]
            e = discord.Embed(
                title=f"\N{GLOBE WITH MERIDIANS} Fortnite Item Shop — {title}",
                description=f"Support the creator **{creator_code}** \N{PURPLE HEART}  | Updates daily at 00:00 UTC",
                color=discord.Color.purple()
            )
            e.set_footer(text="Powered by GalacticModz")

            # Use first item as thumbnail if present
            try:
                thumb = chunk[0]["items"][0]["images"]["icon"]
                if thumb:
                    e.set_thumbnail(url=thumb)
            except Exception:
                pass

            for entry in chunk:
                try:
                    it = entry["items"][0]
                    name = it.get("name", "Unknown")
                    rarity = (it.get("rarity", {}) or {}).get("value", "unknown").title()
                    price = entry.get("finalPrice", "?")
                    e.add_field(name=name, value=f"Rarity: {rarity}\nPrice: {price} V-Bucks", inline=False)
                except Exception:
                    continue

            embeds.append(e)

    if not embeds:
        embeds.append(discord.Embed(
            title="Fortnite Item Shop",
            description="No items found (API empty). Try again later.",
            color=discord.Color.orange()
        ))
    return embeds
