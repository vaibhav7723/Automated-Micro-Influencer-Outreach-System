import sqlite3
import csv
from datetime import datetime, timezone
import config


def init_db():
    conn = sqlite3.connect(config.TRACKER_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS outreach_log (
            influencer_name TEXT,
            contact_email TEXT PRIMARY KEY,
            message_generated INTEGER,
            sent INTEGER,
            date TEXT,
            status TEXT
        )
    """)
    conn.commit()
    return conn


def already_contacted(conn, contact_email):
    if contact_email == "Not Found":
        return False
    row = conn.execute(
        "SELECT 1 FROM outreach_log WHERE contact_email = ?", (contact_email,)
    ).fetchone()
    return row is not None


def log_outreach(conn, name, contact_email, message_generated, sent, status):
    conn.execute(
        """INSERT INTO outreach_log
           (influencer_name, contact_email, message_generated, sent, date, status)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(contact_email) DO UPDATE SET
             sent=excluded.sent, date=excluded.date, status=excluded.status""",
        (name, contact_email, int(message_generated), int(sent),
         datetime.now(timezone.utc).isoformat(), status),
    )
    conn.commit()


def export_csv(conn):
    rows = conn.execute("SELECT * FROM outreach_log").fetchall()
    cols = ["influencer_name", "contact_email", "message_generated", "sent", "date", "status"]
    with open(config.TRACKER_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
