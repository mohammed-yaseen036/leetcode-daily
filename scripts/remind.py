"""remind.py — the escalation reminder engine (Hermes cron runs it frequently).
Logic:
- 7:00 IST: new_day.py sends the morning email (separate cron)
- 10:00-12:00 IST: every 15 min, email "one question remaining" reminders
- 20:00 IST: final evening reminder
- Stops once today is committed."""
import sys, os
from datetime import datetime, date
sys.path.insert(0, os.path.dirname(__file__))
from common import load_state, next_topic_problem, fetch_daily_challenge, send_email, today_str

now = datetime.now()
today = today_str()
st = load_state()
day = st["days"].get(today, {})

if day.get("committed"):
    print(f"{today} already committed — no reminders.")
    sys.exit(0)

if not day.get("prepared"):
    print("Day not prepared yet (new_day hasn't run).")
    sys.exit(0)

mins = now.hour * 60 + now.minute
prob, topic = next_topic_problem(st)
remaining = []
# which of the two is uncommitted? we track per-day flags; assume both until told
daily_done = day.get("daily", False) and day.get("topic_committed", False)
names = f"'{prob['title']}' ({topic['dir']})" if prob else "topic problem"

if 600 <= mins < 720:  # 10:00 - 11:59
    # quarter-hour check handled by cron schedule; just send
    send_email(f"⏰ Reminder: {2 if not daily_done else 1} question(s) left today",
               f"Not committed yet!\n\nStill pending: {names}\nStreak at risk: {st['streak']} days.\nSolve it now: https://leetcode.com")
    print(f"sent 10-12 reminder at {now.strftime('%H:%M')}")
elif mins >= 1200 and mins < 1215:  # 8 PM window
    send_email(f"🌙 Final reminder — {2 if not daily_done else 1} question(s) left",
               f"Last call for {today}. Pending: {names}\nYour streak ({st['streak']} days) dies at midnight. Commit & push!")
    print("sent 8PM reminder")
else:
    print(f"{now.strftime('%H:%M')} — outside reminder windows, nothing sent.")
