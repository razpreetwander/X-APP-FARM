import os, sys, smtplib, ssl
from email.message import EmailMessage

subject = sys.argv[1] if len(sys.argv) > 1 else "update"
body = sys.argv[2] if len(sys.argv) > 2 else ""
attachments = sys.argv[3:]

user = os.environ.get("BOSS_EMAIL", "").strip().strip('"').strip("'")
pw = os.environ.get("EMAIL_APP_PASS", "").replace(" ", "").strip().strip('"').strip("'")

if not user or not pw:
    print("email skipped: BOSS_EMAIL ya EMAIL_APP_PASS secret khali hai")
    sys.exit(0)

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

def via_ssl_465():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30,
                          context=ssl.create_default_context()) as s:
        s.login(user, pw)
        s.send_message(msg)

def via_starttls_587():
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as s:
        s.ehlo()
        s.starttls(context=ssl.create_default_context())
        s.ehlo()
        s.login(user, pw)
        s.send_message(msg)

for name, fn in (("465 SSL", via_ssl_465), ("587 STARTTLS", via_starttls_587)):
    try:
        fn()
        print("email sent via", name, ":", subject)
        break
    except smtplib.SMTPAuthenticationError as e:
        print("email failed (", name, ") LOGIN REJECTED: app password ya email galat hai.", e)
        break
    except Exception as e:
        print("email failed (", name, "):", type(e).__name__, e)
