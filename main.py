"""
main.py
Orchestrates the full pipeline:
Discovery -> Filtering -> Enrichment -> AI Personalization -> Sending -> Tracking
"""

import csv
import config
import discovery
import filtering
import enrichment
import personalization
import sending


def write_csv(path, records, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )
        writer.writeheader()

        for r in records:
            writer.writerow(r)


def main():
    print(f"== Discovery (mode={config.DISCOVERY_MODE}) ==")

    raw = discovery.run_discovery()

    print(f"Discovered {len(raw)} influencer profiles")

    print("\n== Filtering & Classification ==")

    classified = filtering.filter_influencers(raw)

    passed = [
        r for r in classified
        if r["status"] == "PASS"
    ]

    failed = [
        r for r in classified
        if r["status"] == "FAIL"
    ]

    print(f"PASS: {len(passed)}   FAIL: {len(failed)}")

    print("\n== Enrichment ==")

    enriched_all = enrichment.enrich_influencers(classified)

    dataset_fields = [
        "name",
        "platform",
        "follower_count",
        "engagement_rate",
        "niche",
        "contact_email",
        "profile_url",
        "content_themes",
        "status",
        "filter_reasons",
        "audience_age",
        "audience_gender",
        "audience_geography",
        "website",
        "enrichment_completeness",
        "data_source",
    ]

    write_csv(
        config.INFLUENCER_CSV,
        enriched_all,
        dataset_fields
    )

    print(f"Wrote dataset -> {config.INFLUENCER_CSV}")

    print("\n== AI Personalization ==")

    shortlisted = [
        r for r in enriched_all
        if r["status"] == "PASS"
    ]

    personalized = personalization.personalize_influencers(
        shortlisted
    )

    msg_fields = [
        "name",
        "platform",
        "niche",
        "contact_email",
        "email_pitch",
        "instagram_dm",
        "generation_method",
    ]

    write_csv(
        config.MESSAGES_CSV,
        personalized,
        msg_fields
    )

    print(f"Wrote messages -> {config.MESSAGES_CSV}")

    print("\n== Sending Layer ==")

    sent_results = sending.run_sending_layer(
        personalized
    )

    for r in sent_results:
        print(
            f"  {r['name']:20s} | "
            f"{r['contact_email']:35s} | "
            f"{r['send_status']}"
        )

    print(
        f"Outreach tracker -> "
        f"{config.TRACKER_CSV}"
    )

    simulated_or_sent = sum(
        1
        for r in sent_results
        if r["send_status"] in [
            "SIMULATED_SENT",
            "SENT"
        ]
    )

    print("\n== Summary ==")
    print(f"Total discovered:    {len(raw)}")
    print(f"Passed filter:       {len(passed)}")
    print(f"Failed filter:       {len(failed)}")
    print(f"Messages generated:  {len(personalized)}")
    print(f"Emails simulated/sent: {simulated_or_sent}")


if __name__ == "__main__":
    main()
