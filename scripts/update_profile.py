import os
import re
import urllib.request
import json
from datetime import datetime, timezone

USER = os.environ.get("GITHUB_USER", "AarveeWadhwa")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "profile-refresh"
}
if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

def get(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def clean(text, limit=90):
    text = (text or "").replace("|", "\\|").replace("\n", " ").strip()
    return text[:limit] + ("…" if len(text) > limit else "")

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    md = f.read()

repos = get(f"https://api.github.com/users/{USER}/repos?sort=updated&direction=desc&per_page=6")
repos = [r for r in repos if not r.get("fork")][:5]

repo_lines = [
    "| Repository | Description | Language |",
    "|---|---|---|"
]

for r in repos:
    name = r["name"]
    url = r["html_url"]
    desc = clean(r.get("description"), 85) or "No description yet."
    lang = r.get("language") or "—"
    repo_lines.append(f"| [{name}]({url}) | {desc} | `{lang}` |")

repo_block = "\n".join(repo_lines)

events = get(f"https://api.github.com/users/{USER}/events/public?per_page=12")
activity = []

for e in events:
    typ = e.get("type", "")
    repo = e.get("repo", {}).get("name", "")
    if not repo:
        continue
    if typ == "PushEvent":
        commits = len(e.get("payload", {}).get("commits", []))
        activity.append(f"• pushed {commits} commit(s) to `{repo}`")
    elif typ == "PullRequestEvent":
        action = e.get("payload", {}).get("action", "updated")
        activity.append(f"• {action} pull request in `{repo}`")
    elif typ == "IssuesEvent":
        action = e.get("payload", {}).get("action", "updated")
        activity.append(f"• {action} an issue in `{repo}`")
    elif typ == "CreateEvent":
        activity.append(f"• created `{repo}`")
    elif typ == "WatchEvent":
        activity.append(f"• starred `{repo}`")
    if len(activity) >= 6:
        break

if not activity:
    activity = ["• No recent public activity to display."]

activity_block = "```text\n" + "\n".join(activity) + "\n```"

md = re.sub(
    r"<!-- RECENT_REPOS:START -->.*?<!-- RECENT_REPOS:END -->",
    "<!-- RECENT_REPOS:START -->\n" + repo_block + "\n<!-- RECENT_REPOS:END -->",
    md,
    flags=re.S
)

md = re.sub(
    r"<!-- RECENT_ACTIVITY:START -->.*?<!-- RECENT_ACTIVITY:END -->",
    "<!-- RECENT_ACTIVITY:START -->\n" + activity_block + "\n<!-- RECENT_ACTIVITY:END -->",
    md,
    flags=re.S
)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(md)
