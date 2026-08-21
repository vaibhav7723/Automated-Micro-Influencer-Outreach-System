MANDATORY_FIELDS = [
    "name", "platform", "profile_url", "follower_count", "engagement_rate",
    "niche", "content_themes", "contact_email",
]
OPTIONAL_FIELDS = ["website", "audience_age", "audience_gender", "audience_geography"]


def enrich_record(record):
    enriched = dict(record)
    for field in MANDATORY_FIELDS + OPTIONAL_FIELDS:
        if field not in enriched or enriched[field] in (None, ""):
            enriched[field] = "Not Found"

    enriched["has_valid_email"] = enriched["contact_email"] != "Not Found"
    enriched["enrichment_completeness"] = round(
        sum(1 for f in MANDATORY_FIELDS + OPTIONAL_FIELDS if enriched[f] != "Not Found")
        / len(MANDATORY_FIELDS + OPTIONAL_FIELDS) * 100, 1
    )
    return enriched


def enrich_influencers(records):
    return [enrich_record(r) for r in records]
