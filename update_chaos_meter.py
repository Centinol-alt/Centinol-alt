import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# GitHub API setup
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = 'Centinol-alt'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Timezone setting for resetting at midnight BST
TZ = ZoneInfo('Europe/London')
# Current time in BST
now_tz = datetime.now(TZ)
# Midnight today in BST
midnight_tz = now_tz.replace(hour=0, minute=0, second=0, microsecond=0)
# Convert midnight to UTC for comparing event timestamps
midnight_utc = midnight_tz.astimezone(ZoneInfo('UTC'))

# Fetch commits from the last 24 hours
url = f'https://api.github.com/users/{USERNAME}/events'
response = requests.get(url, headers=headers)
events = response.json()

# Count commits (you can adjust this logic for other metrics like issues)
commit_count = sum(
    1 for event in events
    if event['type'] == 'PushEvent'
    and datetime.fromisoformat(event['created_at'].replace('Z', '+00:00')) >= midnight_utc
)

# Calculate chaos level (0-100%)
# Example: 0 commits = 0%, 10+ commits = 100%
chaos_level = min(commit_count * 10, 100)  # Adjust multiplier as needed

# Determine chaos bar color based on level
if chaos_level <= 20:
    bar_color = "#55ff55"  # Green for low chaos
    chaos_text = "All systems green"
    tooltip_text = "Everything's under control... for now."
elif chaos_level <= 60:
    bar_color = "#ffff55"  # Yellow for medium chaos
    chaos_text = "Things are heating up"
    tooltip_text = "I might've forgotten a semicolon somewhere."
else:
    bar_color = "#ff5555"  # Red for high chaos
    # More chaotic messages for high chaos
    if chaos_level <= 80:
        chaos_text = "Send coffee!"
        tooltip_text = "I broke prod again!"
    else:
        chaos_text = "Regex betrayed me!"
        tooltip_text = "I trusted regex, and now I'm paying for it."

# Update SVG file with color, tooltip, and custom message, spanning full width of README
svg_content = f"""<svg width="100%" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="20" width="300" height="20" fill="#444" rx="10"/>
  <rect x="0" y="20" width="{chaos_level}%" height="20" fill="{bar_color}" rx="10" id="chaos-bar">
    <title>{tooltip_text}</title>
  </rect>
  <text x="50%" y="15" font-size="12" fill="#fff" text-anchor="middle" id="chaos-text">{chaos_level}% Chaos: {chaos_text}</text>
</svg>"""

with open('chaos-meter/chaos-meter.svg', 'w') as f:
    f.write(svg_content)