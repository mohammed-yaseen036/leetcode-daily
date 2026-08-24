<div align="center">

# ⚡ LeetCode Daily

**A disciplined, automated DSA practice system — 2 problems every single day, in Python.**

![Streak](https://img.shields.io/badge/dynamic/json?url=file://scripts/state.json&label=streak&query=streak&suffix=%20days&color=brightgreen&style=for-the-badge)
![Problems](https://img.shields.io/badge/problems-4033%20available-blue?style=for-the-badge)
![Language](https://img.shields.io/badge/language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/automation-cron%20%2B%20email-orange?style=for-the-badge)

*One LeetCode Daily Challenge + one topic-wise syllabus problem. Every day. No excuses.*

[Workflow](#-daily-workflow) • [Syllabus](#-the-syllabus) • [Structure](#-repository-structure) • [Stats](#-stats) • [Automation](#-how-the-automation-works)

</div>

---

## 🎯 The System

Most people grind LeetCode randomly and burn out. This repository enforces a
different approach:

1. **Consistency over intensity** — exactly 2 problems per day, tracked by a streak.
2. **Structured progression** — 16 topics in dependency order, easy→hard within each,
   so foundations come before advanced patterns.
3. **Full accountability** — email reminders escalate through the day until the
   daily commit lands; the streak dies at midnight otherwise.

```
 ┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌───────────┐
 │ 7:00 AM  │───▶│ Solve both  │───▶│ commit_day   │───▶│  GitHub   │
 │ email 📩 │    │ on LeetCode │    │ (auto-stats) │    │  push ✅  │
 └──────────┘    └─────────────┘    └──────────────┘    └───────────┘
      │                                   ▲
      │        not committed yet?         │
      └──▶ reminders 10AM–12PM + 8PM ─────┘
```

## 📚 The Syllabus

Sixteen topics, each progressing from foundational Easy problems to Hard ones
before advancing:

| # | Topic | # | Topic |
|---|---|---|---|
| 01 | Arrays & Hashing | 09 | Heap / Priority Queue |
| 02 | Two Pointers | 10 | Backtracking |
| 03 | Sliding Window | 11 | Graphs |
| 04 | Stack | 12 | 1D Dynamic Programming |
| 05 | Binary Search | 13 | 2D Dynamic Programming |
| 06 | Linked List | 14 | Greedy |
| 07 | Trees | 15 | Intervals |
| 08 | Tries | 16 | Math & Bit Manipulation |

## 📂 Repository Structure

```
leetcode-daily/
│
├── daily-challenge/              # LeetCode's official problem of the day
│   └── YYYY-MM-DD/
│       └── solution.py           # approach notes + complexity + solution
│
├── dsa-topics/                   # the sequential 16-topic syllabus
│   ├── 01-arrays-hashing/
│   │   ├── 001-two-sum/solution.py
│   │   └── ...
│   └── ...
│
├── scripts/                      # the automation engine
│   ├── new_day.py                # fetches problems, creates folders, emails list
│   ├── remind.py                 # escalation reminder logic
│   ├── commit_day.py             # commit+push+stats+streak, one command
│   ├── common.py                 # shared state / email / LeetCode API
│   ├── gen_syllabus.py           # builds syllabus.json from full problem set
│   ├── syllabus.json             # 16 topics, 1274 ordered problems
│   └── state.json                # position, streak, history
│
├── STATS.md                      # running log of every solved problem
└── README.md
```

## 🔁 Daily Workflow

| Step | Action | Tool |
|:---:|---|---|
| 1 | **7 AM** — today's two problems arrive by email; folders + boilerplate auto-created | `new_day.py` *(cron)* |
| 2 | Solve both on leetcode.com, paste working code into the prepared `solution.py` files | you 💪 |
| 3 | Run one command — stages, commits (`Day N: ...`), pushes, updates STATS.md & streak | `python scripts/commit_day.py` |
| 4 | Uncommitted? Reminders every 15 min (10–12) then once at 8 PM. Committed? Silence. | `remind.py` *(cron)* |

Every solution file starts with a template that forces good habits:

```python
"""
Problem Name
Link: https://leetcode.com/problems/...

Approach (write before coding!):
1.

Complexity: Time O(?) Space O(?)
"""
class Solution:
    pass
```

## 📊 Stats

Live numbers are maintained automatically in [`STATS.md`](STATS.md):

- Current streak / longest streak
- Total problems solved
- Per-topic progress

<!-- STATS:START -->
<!-- Updated by scripts/commit_day.py — do not edit manually -->
<!-- STATS:END -->

## ⚙️ How the Automation Works

```
Hermes cron jobs (local machine)
 ├── 07:00 IST → new_day.py     → LeetCode GraphQL fetch + folders + email
 ├── */15 10–11 → remind.py     → escalation emails while uncommitted
 └── 20:00 IST → remind.py     → final call before midnight streak death
```

- Problem data comes from LeetCode's public GraphQL API.
- State lives in `scripts/state.json`; the syllabus was generated from the
  complete 4,033-problem catalog filtered to 16 topics and sorted by difficulty.
- Email delivery via Gmail SMTP with an app password.

---

<div align="center">

**"You don't have to be extreme, just consistent."**

*Day 1 started Aug 24, 2026.*

</div>
