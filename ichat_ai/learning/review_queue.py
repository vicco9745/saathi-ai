import json
from pathlib import Path
from ichat_ai.learning.filter import save_approved

QUEUE_FILE = Path("ichat_ai/dataset/learning_queue.jsonl")

if not QUEUE_FILE.exists():
    print("Learning queue खाली है।")
    raise SystemExit

items = []

with open(QUEUE_FILE, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get("user"):
                items.append(data["user"])
        except json.JSONDecodeError:
            pass

if not items:
    print("Learning queue खाली है।")
    raise SystemExit

print("=== Saathi Learning Review ===")

for question in items:
    print("\nसवाल:", question)
    answer = input("सही जवाब: ").strip()

    if save_approved(question, answer):
        print("✅ Approved में सेव हो गया।")
    else:
        print("❌ सेव नहीं हुआ।")

print("\nReview पूरा हुआ।")
