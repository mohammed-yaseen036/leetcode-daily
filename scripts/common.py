"""Shared state helpers for the leetcode-daily automation."""
import json, os
from datetime import date, datetime

REPO = os.path.expanduser("~/leetcode-daily")
STATE = os.path.join(REPO, "scripts", "state.json")
SYL = os.path.join(REPO, "scripts", "syllabus.json")


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"topic_idx": 0, "prob_idx": 0, "streak": 0,
            "longest_streak": 0, "last_done": None,
            "days": {},  # "YYYY-MM-DD": {"daily": true/false, "topic": "..."}
            "total_solved": 0}


def save_state(st):
    json.dump(st, open(STATE, "w"), indent=1)


def load_syllabus():
    return json.load(open(SYL))


def next_topic_problem(st):
    """Return (problem dict, topic dict) for the current position."""
    syl = load_syllabus()
    ti = st["topic_idx"]
    while ti < len(syl):
        probs = syl[ti]["problems"]
        pi = st["prob_idx"] if ti == st["topic_idx"] else 0
        if pi < len(probs):
            return probs[pi], syl[ti]
        ti += 1
    return None, None


def advance(st):
    syl = load_syllabus()
    st["prob_idx"] += 1
    # skip forward across exhausted topics
    while st["topic_idx"] < len(syl) and st["prob_idx"] >= len(syl[st["topic_idx"]]["problems"]):
        st["topic_idx"] += 1
        st["prob_idx"] = 0


def today_str():
    return date.today().isoformat()


def fetch_daily_challenge():
    """LeetCode's official problem of the day via GraphQL."""
    try:
        import urllib.request
        req = urllib.request.Request(
            "https://leetcode.com/graphql",
            data=json.dumps({"query":
                "{ activeDailyCodingChallengeQuestion { date question { title titleSlug difficulty } } }"}).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "Referer": "https://leetcode.com"})
        d = json.loads(urllib.request.urlopen(req, timeout=20).read())
        q = d["data"]["activeDailyCodingChallengeQuestion"]["question"]
        return {"title": q["title"], "slug": q["titleSlug"],
                "difficulty": q["difficulty"].capitalize(),
                "link": f"https://leetcode.com/problems/{q['titleSlug']}/"}
    except Exception as e:
        return {"title": "(fetch failed - check manually)", "slug": "", "difficulty": "?", "link": f"error:{e}"}


def send_email(subject, body):
    import smtplib
    from email.mime.text import MIMEText
    cfg = json.load(open(os.path.expanduser("~/.hermes/leetcode_notify_creds.json")))
    email, pwd = cfg["email"], cfg["app_password"].replace(" ", "")
    msg = MIMEText(body)
    msg["Subject"], msg["From"], msg["To"] = subject, email, email
    s = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
    s.starttls()
    s.login(email, pwd)
    s.send_message(msg)
    s.quit()
