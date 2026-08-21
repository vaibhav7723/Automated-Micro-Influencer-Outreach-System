import random
import requests
import config


def discover_youtube_influencers(niche_keyword, max_results=15, api_key=None):
    api_key = api_key or config.YOUTUBE_API_KEY
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY not set — cannot run live discovery.")

    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "q": niche_keyword,
        "type": "channel",
        "maxResults": min(max_results, 50),
        "key": api_key,
    }
    resp = requests.get(search_url, params=search_params, timeout=15)
    resp.raise_for_status()
    channel_ids = [item["snippet"]["channelId"] for item in resp.json().get("items", [])]
    if not channel_ids:
        return []

    stats_url = "https://www.googleapis.com/youtube/v3/channels"
    stats_params = {
        "part": "snippet,statistics,brandingSettings",
        "id": ",".join(channel_ids),
        "key": api_key,
    }
    stats_resp = requests.get(stats_url, params=stats_params, timeout=15)
    stats_resp.raise_for_status()

    results = []
    for item in stats_resp.json().get("items", []):
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        subs = int(stats.get("subscriberCount", 0)) if not stats.get("hiddenSubscriberCount") else 0
        results.append({
            "name": snippet.get("title", "Unknown"),
            "platform": "YouTube",
            "profile_url": f"https://youtube.com/channel/{item['id']}",
            "follower_count": subs,
            "video_count": int(stats.get("videoCount", 0)),
            "view_count": int(stats.get("viewCount", 0)),
            "niche": niche_keyword,
            "bio": snippet.get("description", ""),
            "data_source": "LIVE_YOUTUBE_API",
        })
    return results


def discover_instagram_stub(niche_keyword):
    raise NotImplementedError(
        "Instagram discovery requires a licensed marketplace API "
        "(e.g. Collabstr/Aspire/Grin) or Meta Graph API with proper "
        "permissions. Not implemented here to avoid ToS-violating scraping."
    )


_FIRST_NAMES = ["Sarah", "Maya", "Alex", "Priya", "Jordan", "Liam", "Zoe", "Kabir",
                "Nina", "Ravi", "Emma", "Diego", "Aisha", "Noah", "Sofia", "Arjun",
                "Chloe", "Marcus", "Ines", "Yuki"]
_LAST_NAMES = ["Verma", "Lee", "Garcia", "Khan", "Cole", "Patel", "Rossi", "Kim",
               "Singh", "Brown", "Nakamura", "Alvarez", "Sharma", "Nguyen", "Reed"]

_NICHE_THEMES = {
    "Fitness": ["home workouts", "marathon training", "mobility routines", "gym form checks"],
    "Fintech": ["personal budgeting", "index fund investing", "credit score tips", "startup finance"],
    "Beauty": ["skincare routines", "clean makeup looks", "product dupes", "haircare tips"],
    "Fashion": ["capsule wardrobes", "thrift styling", "seasonal lookbooks", "sneaker reviews"],
    "Technology": ["gadget unboxings", "productivity apps", "AI tool reviews", "budget tech picks"],
}

_PLATFORMS = ["Instagram", "YouTube", "TikTok"]


def discover_sample_influencers(niches=None, count=55, seed=42):
    rng = random.Random(seed)
    niches = niches or config.NICHES
    records = []
    for i in range(count):
        niche = niches[i % len(niches)]
        first = rng.choice(_FIRST_NAMES)
        last = rng.choice(_LAST_NAMES)
        handle = f"{first.lower()}.{last.lower()}{rng.randint(1,99)}"
        platform = rng.choice(_PLATFORMS)
        followers = rng.randint(4_500, 105_000)
        engagement = round(rng.uniform(0.4, 7.5), 2)
        theme = rng.choice(_NICHE_THEMES[niche])
        has_email = rng.random() < 0.55
        email = f"collabs.{handle}@creatormail.com" if has_email else "Not Found"

        records.append({
            "name": f"{first} {last}",
            "platform": platform,
            "profile_url": f"https://{platform.lower()}.com/{handle}",
            "follower_count": followers,
            "engagement_rate": engagement,
            "niche": niche,
            "content_themes": theme,
            "contact_email": email,
            "website": f"https://{handle}.com" if rng.random() < 0.3 else "Not Found",
            "audience_age": rng.choice(["18-24", "25-34", "35-44", "Not Found"]),
            "audience_gender": rng.choice(["Mostly Female", "Mostly Male", "Balanced", "Not Found"]),
            "audience_geography": rng.choice(["US", "India", "UK", "Global", "Not Found"]),
            "recent_content_note": f"recent post/video about {theme}",
            "data_source": "SAMPLE_DEMO",
        })
    return records


def run_discovery():
    if config.DISCOVERY_MODE == "live":
        all_results = []
        for niche in config.NICHES:
            try:
                all_results.extend(discover_youtube_influencers(niche))
            except Exception as e:
                print(f"[discovery] live fetch failed for {niche}: {e}")
        return all_results
    else:
        return discover_sample_influencers(count=55)
