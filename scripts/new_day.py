"""new_day.py — run each morning (cron does it at 7 AM IST).
Fetches today's daily challenge + next syllabus problem, creates folders,
sends the 7 AM email."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (REPO, load_state, save_state, next_topic_problem,
                    fetch_daily_challenge, today_str, send_email)

today = today_str()
st = load_state()

# already prepared?
if st["days"].get(today, {}).get("prepared"):
    print(f"{today} already prepared")
    sys.exit(0)

daily = fetch_daily_challenge()
prob, topic = next_topic_problem(st)

# create folders + boilerplate
def boiler(name, link, kind):
    return f'''"""
{name}
{kind}
Link: {link}

Approach (write before coding!):
1.

Complexity: Time O(?) Space O(?)
"""

\nclass Solution:
    pass
'''

if daily["slug"]:
    d = os.path.join(REPO, "daily-challenge", today)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "solution.py"), "w").write(
        boiler(daily["title"], daily["link"], "LeetCode Daily Challenge"))

if prob:
    d = os.path.join(REPO, topic["dir"], f"{st['prob_idx']+1:03d}-{prob['slug']}")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "solution.py"), "w").write(
        boiler(prob["title"], f"https://leetcode.com/problems/{prob['slug']}/",
               f"DSA Topic: {topic['dir']} #{st['prob_idx']+1}/{len(topic['problems'])}"))

st.setdefault("days", {})[today] = {"prepared": True, "committed": False}
save_state(st)

body = f"""Good morning! Your 2 problems for {today}:

1. DAILY CHALLENGE: {daily['title']} [{daily['difficulty']}]
   {daily['link']}

2. TOPIC PROBLEM ({topic['dir'] if topic else 'syllabus complete!'}): {prob['title'] if prob else '-'} [{prob['difficulty'] if prob else ''}]
   https://leetcode.com/problems/{prob['slug']}/

Solve both, then commit & push. Streak: {st['streak']} days (best: {st['longest_streak']})
Reminder emails: 10-12 every 15 min if not committed, final one at 8 PM.
"""
send_email(f"LeetCode Daily - {today} - 2 problems await", body)
print(body)
