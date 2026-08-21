import config

BRAND_FIT_NICHES = {"Beauty", "Fashion"}


def classify_influencer(record):
    reasons = []
    followers = record.get("follower_count", 0)
    engagement = record.get("engagement_rate", 0)
    niche = record.get("niche", "")

    if not (config.MIN_FOLLOWERS <= followers <= config.MAX_FOLLOWERS):
        reasons.append(
            f"Follower count {followers:,} outside micro-influencer range "
            f"({config.MIN_FOLLOWERS:,}-{config.MAX_FOLLOWERS:,})"
        )

    if engagement < config.MIN_ENGAGEMENT_RATE:
        reasons.append(
            f"Engagement rate {engagement}% below minimum threshold "
            f"({config.MIN_ENGAGEMENT_RATE}%)"
        )

    if niche not in config.NICHES:
        reasons.append(f"Niche '{niche}' not in target category list")

    if niche in BRAND_FIT_NICHES:
        audience_signals = [
            record.get("audience_age", "Not Found"),
            record.get("audience_gender", "Not Found"),
            record.get("audience_geography", "Not Found"),
        ]
        if all(v == "Not Found" for v in audience_signals):
            reasons.append("Beauty/Fashion brand-fit rule: no audience demographic data available")

    record["status"] = "PASS" if not reasons else "FAIL"
    record["filter_reasons"] = "; ".join(reasons) if reasons else "Meets all filtering criteria"
    return record


def filter_influencers(records):
    return [classify_influencer(r) for r in records]
