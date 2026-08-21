import json
import config

try:
    import anthropic
    _HAS_SDK = True
except ImportError:
    _HAS_SDK = False


EMAIL_SYSTEM_PROMPT = """You write short, warm, non-generic influencer collaboration \
outreach emails for a brand partnerships team. Output ONLY valid JSON, no markdown fences, \
no preamble. Never invent facts not given to you."""

EMAIL_USER_TEMPLATE = """Write a personalized brand collaboration outreach email and a short \
Instagram DM for this influencer. Use the details below — do not invent additional facts.

Name: {name}
Platform: {platform}
Niche: {niche}
Content themes: {content_themes}
Recent content note: {recent_content_note}
Follower count: {follower_count}
Engagement rate: {engagement_rate}%
Audience geography: {audience_geography}

Requirements:
- email_pitch: 60-90 words, references their niche/content style, proposes a specific \
collaboration angle (choose the best fit among sponsorship, affiliate campaign, UGC content, \
brand ambassador program, paid placement, or barter), and states a clear value proposition.
- instagram_dm: 15-30 words, short, natural, casual tone, personalized.

Return strictly this JSON shape:
{{"email_pitch": "...", "instagram_dm": "..."}}"""


def _call_claude(record):
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=EMAIL_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": EMAIL_USER_TEMPLATE.format(**record),
        }],
    )
    text = "".join(block.text for block in resp.content if block.type == "text")
    text = text.strip().strip("```").replace("json\n", "", 1) if text.strip().startswith("```") else text
    return json.loads(text)


def _fallback_generate(record):
    name_first = record["name"].split(" ")[0]
    theme = record.get("content_themes", "your content")
    niche = record.get("niche", "your niche")

    email_pitch = (
        f"Hi {name_first}, I've been following your {niche.lower()} content, especially your "
        f"work on {theme} — the tone feels authentic and clearly resonates with your audience. "
        f"We're building a UGC/affiliate collaboration for a {niche.lower()}-focused launch and "
        f"think your community ({record.get('follower_count', 0):,} followers, "
        f"{record.get('engagement_rate', 0)}% engagement) is a strong fit. Would you be open to "
        f"a quick call to explore a paid partnership or barter collaboration?"
    )
    instagram_dm = (
        f"Hi {name_first}! Loved your {theme} content — your audience feels like a great fit "
        f"for a {niche.lower()} collab we're launching. Open to chatting?"
    )
    return {"email_pitch": email_pitch, "instagram_dm": instagram_dm}


def generate_messages(record):
    if config.ANTHROPIC_API_KEY and _HAS_SDK:
        try:
            result = _call_claude(record)
            result["generation_method"] = "LLM_CLAUDE"
            return result
        except Exception as e:
            print(f"[personalization] Claude call failed for {record.get('name')}: {e} — using fallback")
    result = _fallback_generate(record)
    result["generation_method"] = "FALLBACK_TEMPLATE"
    return result


def personalize_influencers(records):
    output = []
    for r in records:
        messages = generate_messages(r)
        merged = dict(r)
        merged["email_pitch"] = messages["email_pitch"]
        merged["instagram_dm"] = messages["instagram_dm"]
        merged["generation_method"] = messages["generation_method"]
        output.append(merged)
    return output
