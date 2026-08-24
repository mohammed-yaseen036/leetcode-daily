"""Generate topic-wise syllabus.json — ordered easy->hard within each topic."""
import json, os
from collections import defaultdict

SRC = os.path.expanduser("~/Desktop/dsa with python leetcode full/leetcode_all.json")
OUT = os.path.expanduser("~/leetcode-daily/scripts/syllabus.json")

TOPICS = [  # (syllabus name, {matching leetcode tags})
    ("01-arrays-hashing", {"Array", "Hash Table", "Counting"}),
    ("02-two-pointers", {"Two Pointers"}),
    ("03-sliding-window", {"Sliding Window"}),
    ("04-stack", {"Stack", "Monotonic Stack"}),
    ("05-binary-search", {"Binary Search"}),
    ("06-linked-list", {"Linked List", "Doubly-Linked List"}),
    ("07-trees", {"Tree", "Binary Tree", "Binary Search Tree", "DFS", "BFS"}),
    ("08-tries", {"Trie"}),
    ("09-heap", {"Heap (Priority Queue)"}),
    ("10-backtracking", {"Backtracking", "Recursion"}),
    ("11-graphs", {"Graph Theory", "Union-Find", "Topological Sort", "Shortest Path", "Matrix"}),
    ("12-1d-dp", {"Dynamic Programming", "Memoization"}),
    ("13-2d-dp", {"Dynamic Programming"}),
    ("14-greedy", {"Greedy"}),
    ("15-intervals", {"Greedy", "Sorting", "Sweep Line"}),
    ("16-math-bit", {"Math", "Bit Manipulation", "Number Theory"}),
]

qs = json.load(open(SRC))
diff_rank = {"EASY": 0, "MEDIUM": 1, "HARD": 2}
syllabus = []
seen = set()
for idx, (slug, tags) in enumerate(TOPICS):
    probs = {}
    for q in qs:
        qtags = {t["name"] for t in q["topicTags"]}
        # primary-topic problems only for specialized lists like tries
        strict = slug in ("08-tries",)
        match = qtags & tags
        if not match:
            continue
        if strict and len(match & tags) < 1:
            continue
        # weight: fraction of tags matching decides relevance
        score = len(match) / len(qtags | tags)
        if score < 0.34 and slug not in ("13-2d-dp",):
            continue
        key = q["titleSlug"]
        if key in seen:
            continue
        seen.add(key)
        probs[key] = {
            "slug": key,
            "title": q.get("title", key),
            "difficulty": q["difficulty"].capitalize(),
            "topic_dir": f"dsa-topics/{slug}",
        }
    ordered = sorted(probs.values(), key=lambda p: diff_rank[p["difficulty"].upper()])
    # split DP: 1d-dp takes easy+medium, 2d-dp takes the hard ones
    if slug == "12-1d-dp":
        ordered = [p for p in ordered if p["difficulty"] != "Hard"]
    if slug == "13-2d-dp":
        ordered = [p for p in probs.values() if p["difficulty"] == "Hard"]
        ordered.sort(key=lambda p: diff_rank["HARD"])
    syllabus.append({"dir": slug, "count": len(ordered), "problems": ordered})

json.dump(syllabus, open(OUT, "w"), indent=1)
total = sum(t["count"] for t in syllabus)
print(f"syllabus: {len(syllabus)} topics, {total} problems")
for t in syllabus:
    e = sum(1 for p in t['problems'][:5])
    print(t["dir"], t["count"], "| starts:", t["problems"][0]["slug"] if t["problems"] else "-")
