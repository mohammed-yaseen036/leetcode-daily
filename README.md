# LeetCode Daily

A disciplined daily LeetCode practice system: one official Daily Challenge plus
one problem from a topic-wise DSA syllabus (easy to hard within each topic,
16 topics in sequence), solved in Python and pushed here every day.

## Current Status

| Metric | Value |
|---|---|
| Current streak | updated automatically by `scripts/commit_day.py` |
| Longest streak | see `STATS.md` |
| Total problems | see `STATS.md` |

## Repository Structure

```
leetcode-daily/
├── daily-challenge/        # LeetCode's official problem of the day
│   └── YYYY-MM-DD/solution.py
├── dsa-topics/             # the sequential syllabus
│   ├── 01-arrays-hashing/NNN-problem-slug/solution.py
│   ├── 02-two-pointers/
│   └── ... (16 topics)
├── scripts/                # automation (new_day, commit_day, reminders)
└── STATS.md                # running log of every solved problem
```

## Syllabus Order

1. Arrays & Hashing
2. Two Pointers
3. Sliding Window
4. Stack
5. Binary Search
6. Linked List
7. Trees
8. Tries
9. Heap / Priority Queue
10. Backtracking
11. Graphs
12. 1D DP
13. 2D DP
14. Greedy
15. Intervals
16. Math & Bit Manipulation

Each topic starts with foundational Easy problems and progresses to Hard ones
before moving to the next topic.

## Daily Workflow

1. **7:00 AM** — `scripts/new_day.py` fetches today's two problems, creates the
   folders with boilerplate, emails me the list.
2. **Solve both** on leetcode.com, paste working solutions into the prepared
   `solution.py` files.
3. **Commit** — run `python scripts/commit_day.py`. It stages, commits with a
   standardized message, pushes, appends to `STATS.md`, advances the syllabus
   position, and updates the streak.
4. **Reminders** — if not committed: every 15 min from 10 AM–12 PM, then once
   at 8 PM. Stops when today's push lands.
