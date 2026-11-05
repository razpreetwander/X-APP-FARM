import os, sys, smtplib, ssl
from email.message import EmailMessage

subject = sys.argv[1] if len(sys.argv) > 1 else "update"
body = sys.argv[2] if len(sys.argv) > 2 else ""
attachments = sys.argv[3:]

try:
    user = os.environ["BOSS_EMAIL"].strip()
    pw = os.environ["EMAIL_APP_PASS"].replace(" ", "").strip()
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = user
    msg["Subject"] = "[APK Analyzer] " + subject
    msg.set_content(body[:30000] or "(no details)")
    for p in attachments:
        if os.path.isfile(p) and os.path.getsize(p) < 15 * 1024 * 1024:
            with open(p, "rb") as f:
                msg.add_attachment(f.read(), maintype="text", subtype="plain",
                                   filename=os.path.basename(p))
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as s:
        s.login(user, pw)
        s.send_message(msg)
    print("email sent:", subject)
except Exception as e:
    print("email failed:", type(e).__name__, e)
