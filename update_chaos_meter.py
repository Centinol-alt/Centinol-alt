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

# Calculate chaos level based on commit thresholds
if commit_count >= 25:
    chaos_level = 100
elif commit_count >= 15:
    chaos_level = 70
elif commit_count >= 10:
    chaos_level = 50
elif commit_count >= 5:
    chaos_level = 20
else:
    # Scale commits up to 20% for 0-4 commits
    chaos_level = int((commit_count / 5) * 20)

# Determine chaos bar color based on level
# Low chaos (≤20%)
if chaos_level <= 20:
    bar_color = "#55ff55"  # Green
    chaos_text = "Clocking in: all good"
    tooltip_text = "Everything's under control... for now."
# Medium chaos (≤50%)
elif chaos_level <= 50:
    bar_color = "#ffff55"  # Yellow
    chaos_text = "Things are heating up"
    tooltip_text = "I might've forgotten a semicolon somewhere."
# Higher chaos (≤70%)
elif chaos_level <= 70:
    bar_color = "#ffaa00"  # Orange
    chaos_text = "Send coffee!"
    tooltip_text = "I broke prod again!"
# Severe chaos (>70%)
else:
    bar_color = "#ff5555"  # Red
    # More chaotic messages for severe chaos
    if chaos_level < 100:
        chaos_text = "Blyat: idi nahui!"
        tooltip_text = "I trusted regex, and now I'm paying for it."
    else:
        chaos_text = "Absolute chaos!"
        tooltip_text = "There's no turning back now."

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