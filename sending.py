import smtplib
from email.mime.text import MIMEText
import config
import tracker


def _send_email_smtp(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"{config.SENDER_NAME} <{config.SMTP_USER}>"
    msg["To"] = to_email

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_USER, [to_email], msg.as_string())


def run_sending_layer(records):
    conn = tracker.init_db()
    results = []

    for r in records:
        email = r.get("contact_email", "Not Found")
        subject = f"Collaboration idea for {r.get('name', 'you')} x our brand"
        body = r.get("email_pitch", "")

        if email == "Not Found":
            r["send_status"] = "SKIPPED_NO_EMAIL"
            results.append(r)
            continue

        if tracker.already_contacted(conn, email):
            r["send_status"] = "SKIPPED_DUPLICATE"
            results.append(r)
            continue

        if config.DRY_RUN:
            status = "SIMULATED_SENT"
            sent_flag = True
        else:
            try:
                _send_email_smtp(email, subject, body)
                status = "SENT"
                sent_flag = True
            except Exception as e:
                status = f"FAILED: {e}"
                sent_flag = False

        tracker.log_outreach(
            conn, r.get("name", ""), email,
            message_generated=True, sent=sent_flag, status=status,
        )
        r["send_status"] = status
        results.append(r)

    tracker.export_csv(conn)
    conn.close()
    return results
