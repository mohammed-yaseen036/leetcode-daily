"""commit_day.py — stage/commit/push today's work, update STATS.md + streak.
Usage: python commit_day.py [optional custom message]"""
import sys, os, subprocess, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, load_state, save_state, next_topic_problem, today_str

today = today_str()
st = load_state()
custom = " ".join(sys.argv[1:]) or None

# figure out what was done today
day = st["days"].setdefault(today, {"prepared": True, "committed": False})
daily_slug = ""
daily_title = ""
dc_dir = os.path.join(REPO, "daily-challenge", today)
if os.path.isdir(dc_dir):
    for f in os.listdir(dc_dir):
        if f.endswith(".py"):
            daily_slug = f
            head = open(os.path.join(dc_dir, f)).read(200)
            daily_title = head.split('"')[1] if '"' in head else daily_slug

prob, topic = next_topic_problem(st)
topic_title = prob["title"] if prob else "-"

# STATS.md entry
stats_path = os.path.join(REPO, "STATS.md")
if not os.path.exists(stats_path):
    open(stats_path, "w").write("# Stats Log\n\n| Date | Problem | Topic | Difficulty |\n|---|---|---|---|\n")
with open(stats_path, "a") as f:
    if daily_title:
        f.write(f"| {today} | {daily_title} | Daily Challenge | ? |\n")
    if prob:
        f.write(f"| {today} | {prob['title']} | {topic['dir']} | {prob['difficulty']} |\n")

# commit + push
subprocess.run(["git", "add", "-A"], cwd=REPO, check=True)
msg = custom or f"Day {st['streak']+1}: {daily_title or 'daily'} + {topic_title} ({datetime.now().strftime('%d %b')})"
r = subprocess.run(["git", "commit", "-m", msg], cwd=REPO, capture_output=True, text=True)
print(r.stdout or r.stderr)
p = subprocess.run(["git", "push"], cwd=REPO, capture_output=True, text=True)
print(p.stdout or p.stderr)

# update streak only once per day
if not day.get("committed"):
    day["committed"] = True
    day["daily"] = bool(daily_title)
    day["topic"] = prob["slug"] if prob else None
    last = st.get("last_done")
    from datetime import date as _d
    yest = (_d.today().toordinal() - 1) == (_d.fromisoformat(last).toordinal() if last else 0)
    st["streak"] = st.get("streak", 0) + 1 if (last is None or yest) else 1
    st["last_done"] = today
    st["longest_streak"] = max(st["longest_streak"], st["streak"])
    st["total_solved"] = st.get("total_solved", 0) + 2
    # advance syllabus position
    from common import advance
    advance(st)
    save_state(st)

print(f"Streak: {st['streak']} (best {st['longest_streak']}). Committed & pushed: {msg}")
